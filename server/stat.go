package main

import (
	"math"
)

const (
	avgWindSpeed = iota
	minWindSpeed
	maxWindSpeed
	temperature
	gas
	relativeHumidity
	pressure
)

func eliminateOutliers(weather []Weather) []Weather {
	means := computeMeans(weather)
	stdDevs := computeStdDevs(weather, means)

	weather1 := make([]Weather, 0)
	for _, w := range weather {
		if !isOutlier(means[avgWindSpeed], stdDevs[avgWindSpeed], w.AvgWindSpeed) &&
			!isOutlier(means[minWindSpeed], stdDevs[avgWindSpeed], w.MinWindSpeed) &&
			!isOutlier(means[maxWindSpeed], stdDevs[maxWindSpeed], w.MaxWindSpeed) &&
			!isOutlier(means[temperature], stdDevs[temperature], w.Temperature) &&
			!isOutlier(means[gas], stdDevs[gas], w.Gas) &&
			!isOutlier(means[relativeHumidity], stdDevs[relativeHumidity], w.RelativeHumidity) &&
			!isOutlier(means[pressure], stdDevs[pressure], w.Pressure) {
			weather1 = append(weather1, w)
		}
	}

	return weather1
}

func computeMeans(weather []Weather) map[int]float64 {
	n := float64(len(weather))

	means := map[int]float64{
		avgWindSpeed:     0,
		minWindSpeed:     0,
		maxWindSpeed:     0,
		temperature:      0,
		gas:              0,
		relativeHumidity: 0,
		pressure:         0,
	}

	for _, w := range weather {
		means[avgWindSpeed] += w.AvgWindSpeed
		means[minWindSpeed] += w.MinWindSpeed
		means[maxWindSpeed] += w.MaxWindSpeed
		means[temperature] += w.Temperature
		means[gas] += w.Gas
		means[relativeHumidity] += w.RelativeHumidity
		means[pressure] += w.Pressure
	}

	for k, v := range means {
		means[k] = v / n
	}

	return means
}

func computeStdDevs(weather []Weather, means map[int]float64) map[int]float64 {
	n := float64(len(weather))
	stdDeviations := map[int]float64{
		avgWindSpeed:     0,
		minWindSpeed:     0,
		maxWindSpeed:     0,
		temperature:      0,
		gas:              0,
		relativeHumidity: 0,
		pressure:         0,
	}
	for _, w := range weather {
		stdDeviations[avgWindSpeed] += math.Pow(w.AvgWindSpeed-means[avgWindSpeed], 2)
		stdDeviations[minWindSpeed] += math.Pow(w.MinWindSpeed-means[minWindSpeed], 2)
		stdDeviations[maxWindSpeed] += math.Pow(w.MaxWindSpeed-means[maxWindSpeed], 2)
		stdDeviations[temperature] += math.Pow(w.Temperature-means[temperature], 2)
		stdDeviations[gas] += math.Pow(w.Gas-means[gas], 2)
		stdDeviations[relativeHumidity] += math.Pow(w.RelativeHumidity-means[relativeHumidity], 2)
		stdDeviations[pressure] += math.Pow(w.Pressure-means[pressure], 2)
	}

	for k, v := range stdDeviations {
		stdDeviations[k] = math.Sqrt(v / n)
	}
	return stdDeviations
}

func isOutlier(mean, stdDev, val float64) bool {
	max := mean + (3 * stdDev)
	min := mean - (3 * stdDev)
	return val > max || val < min
}
