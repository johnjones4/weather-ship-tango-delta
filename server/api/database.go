package main

import (
	"context"
	"fmt"
	"os"
	"time"

	"github.com/jackc/pgx/v4/pgxpool"
)

var pool *pgxpool.Pool

func connect() {
	_pool, err := pgxpool.Connect(context.Background(), os.Getenv("DATABASE_URL"))
	if err != nil {
		fmt.Println(err)
	}
	pool = _pool
}

func timeoutContext() (context.Context, context.CancelFunc) {
	return context.WithTimeout(context.Background(), time.Duration(time.Second*10))
}

func getWeatherInRange(start time.Time, end time.Time) ([]Weather, error) {
	ctx, cancel := timeoutContext()
	defer cancel()
	rows, err := pool.Query(ctx, "SELECT timestamp, uptime, avg_wind_speed, min_wind_speed, max_wind_speed, temperature, gas, relative_humidity, pressure FROM weather WHERE timestamp >= $1 AND timestamp <= $2", start, end)
	if err != nil {
		return make([]Weather, 0), err
	}
	defer rows.Close()
	output := make([]Weather, 0)
	for rows.Next() {
		w := Weather{}
		err = rows.Scan(&w.Timestamp, &w.Uptime, &w.AvgWindSpeed, &w.MinWindSpeed, &w.MaxWindSpeed, &w.Temperature, &w.Gas, &w.RelativeHumidity, &w.Pressure)
		if err != nil {
			return make([]Weather, 0), err
		}
		output = append(output, w)
	}
	return output, nil
}

func insertWeatherData(weather Weather) error {
	ctx, cancel := timeoutContext()
	defer cancel()
	_, err := pool.Exec(ctx, "INSERT INTO weather (timestamp, uptime, avg_wind_speed, min_wind_speed, max_wind_speed, temperature, gas, relative_humidity, pressure) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)",
		weather.Timestamp,
		weather.Uptime,
		weather.AvgWindSpeed,
		weather.MinWindSpeed,
		weather.MaxWindSpeed,
		weather.Temperature,
		weather.Gas,
		weather.RelativeHumidity,
		weather.Pressure,
	)
	return err
}

func getRebootCount(start time.Time, end time.Time) (int, error) {
	ctx, cancel := timeoutContext()
	defer cancel()
	rows, err := pool.Query(ctx, "SELECT count(*) FROM weather WHERE uptime = 60000 AND timestamp >= $1 AND timestamp <= $2", start, end)
	if err != nil {
		return 0, err
	}
	defer rows.Close()
	if rows.Next() {
		var count int
		rows.Scan(&count)
		return count, nil
	}
	return 0, nil
}

func getDowntimeStats(start time.Time, end time.Time) (DowntimeStats, error) {
	ctx, cancel := timeoutContext()
	defer cancel()
	rows, err := pool.Query(ctx, "SELECT timestamp FROM weather WHERE timestamp >= $1 AND timestamp <= $2", start, end)
	if err != nil {
		return DowntimeStats{}, err
	}
	defer rows.Close()
	timestamps := make([]time.Time, 0)
	for rows.Next() {
		var timestamp time.Time
		rows.Scan(&timestamp)
		timestamps = append(timestamps, timestamp)
	}
	if len(timestamps) < 2 {
		return DowntimeStats{}, nil
	}
	lastTime := timestamps[0].Unix()
	maxTime := 0.0
	longTotal := 0.0
	longCount := 0
	total := 0.0
	for i := 1; i < len(timestamps); i++ {
		time := timestamps[i].Unix()
		space := float64(time - lastTime)
		total += space
		if space > 70 {
			longTotal += space
			longCount++
		}
		if space > maxTime {
			maxTime = space
		}
		lastTime = time
	}
	return DowntimeStats{
		AverageGaps:     total / float64(len(timestamps)-1),
		LongGaps:        longCount,
		AverageLongGaps: longTotal / float64(longCount),
		MaxLongGap:      maxTime,
	}, nil
}

func isStationDown() (bool, error) {
	ctx, cancel := timeoutContext()
	defer cancel()
	twoMinutesAgo := time.Now().UTC().Add(-60 * time.Minute)
	rows, err := pool.Query(ctx, "SELECT count(*) FROM weather WHERE timestamp >= $1", twoMinutesAgo)
	if err != nil {
		return false, err
	}
	defer rows.Close()
	if !rows.Next() {
		return true, nil
	}
	var c int
	rows.Scan(&c)
	return c == 0, nil
}
