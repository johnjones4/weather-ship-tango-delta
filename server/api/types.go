package main

import (
	"time"
)

type Weather struct {
	Timestamp        time.Time `json:"timestamp"`
	Uptime           int64     `json:"uptime"`
	AvgWindSpeed     float64   `json:"avg_wind_speed"`
	MinWindSpeed     float64   `json:"min_wind_speed"`
	MaxWindSpeed     float64   `json:"max_wind_speed"`
	Temperature      float64   `json:"temperature"`
	Gas              float64   `json:"gas"`
	RelativeHumidity float64   `json:"relative_humidity"`
	Pressure         float64   `json:"pressure"`
}

type averageWeather struct {
	avgWindSpeed     float64
	minWindSpeed     float64
	maxWindSpeed     float64
	temperature      float64
	gas              float64
	relativeHumidity float64
	pressure         float64
}

type AverageWeatherValue struct {
	Current  float64 `json:"current_value"`
	Previous float64 `json:"previous_value"`
}

type AverageWeatherResponse struct {
	AvgWindSpeed     AverageWeatherValue `json:"avg_wind_speed"`
	MinWindSpeed     AverageWeatherValue `json:"min_wind_speed"`
	MaxWindSpeed     AverageWeatherValue `json:"max_wind_speed"`
	Temperature      AverageWeatherValue `json:"temperature"`
	Gas              AverageWeatherValue `json:"gas"`
	RelativeHumidity AverageWeatherValue `json:"relative_humidity"`
	Pressure         AverageWeatherValue `json:"pressure"`
}

type DowntimeStats struct {
	AverageGaps     float64 `json:"averageGaps"`
	LongGaps        int     `json:"longGaps"`
	AverageLongGaps float64 `json:"averageLongGaps"`
	MaxLongGap      float64 `json:"maxLongGap"`
}

type ServerInfo struct {
	Downtime DowntimeStats `json:"downtime"`
	Reboots  int           `json:"reboots"`
}

type Message struct {
	Error   bool   `json:"error"`
	Message string `json:"message"`
}

type HTTPReqInfo struct {
	method    string
	uri       string
	referer   string
	ipaddr    string
	code      int
	size      int64
	duration  time.Duration
	userAgent string
}
