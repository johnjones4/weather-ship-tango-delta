package main

import (
	"encoding/json"
	"fmt"
	"math"
	"net/http"
	"sort"
	"strings"
	"time"

	"github.com/felixge/httpsnoop"
)

func logRequestHandler(h http.Handler) http.Handler {
	fn := func(w http.ResponseWriter, r *http.Request) {
		ri := &HTTPReqInfo{
			method:    r.Method,
			uri:       r.URL.String(),
			referer:   r.Header.Get("Referer"),
			userAgent: r.Header.Get("User-Agent"),
		}

		ri.ipaddr = requestGetRemoteAddress(r)

		m := httpsnoop.CaptureMetrics(h, w, r)

		ri.code = m.Code
		ri.size = m.Written
		ri.duration = m.Duration

		fmt.Printf("%s - - [%s] \"%s %s\" %d %d\n", ri.ipaddr, time.Now().Format(time.RFC3339), ri.method, ri.uri, ri.code, ri.size)
	}
	return http.HandlerFunc(fn)
}

func ipAddrFromRemoteAddr(s string) string {
	idx := strings.LastIndex(s, ":")
	if idx == -1 {
		return s
	}
	return s[:idx]
}

func requestGetRemoteAddress(r *http.Request) string {
	hdr := r.Header
	hdrRealIP := hdr.Get("X-Real-Ip")
	hdrForwardedFor := hdr.Get("X-Forwarded-For")
	if hdrRealIP == "" && hdrForwardedFor == "" {
		return ipAddrFromRemoteAddr(r.RemoteAddr)
	}
	if hdrForwardedFor != "" {
		parts := strings.Split(hdrForwardedFor, ",")
		for i, p := range parts {
			parts[i] = strings.TrimSpace(p)
		}
		return parts[0]
	}
	return hdrRealIP
}

func errorResponse(w http.ResponseWriter, err error) {
	w.WriteHeader(http.StatusInternalServerError)
	jsonResponse(w, Message{
		Error:   true,
		Message: fmt.Sprint(err),
	})
}

func jsonResponse(w http.ResponseWriter, info interface{}) {
	jsonInfo, err := json.Marshal(info)
	if err != nil {
		fmt.Println(err)
		return
	}
	w.Header().Add("Content-type", "application/json")
	w.Write(jsonInfo)
}

func truncatedMean(values []float64, p float64) float64 {
	sort.Float64s(values)
	k := int(math.Ceil(float64(len(values)) * p))
	total := 0.0
	r := len(values) - (k * 2)
	for i := k; i < r; i++ {
		total += values[i]
	}
	return total / float64(r)
}

func mapWeatherValue(ws []Weather, m func(w Weather) float64) []float64 {
	arr := make([]float64, len(ws))
	for i, w := range ws {
		arr[i] = m(w)
	}
	return arr
}

func determineAverageWeather(ws []Weather) averageWeather {
	avgWindSpeeds := mapWeatherValue(ws, func(w Weather) float64 { return w.AvgWindSpeed })
	minWindSpeeds := mapWeatherValue(ws, func(w Weather) float64 { return w.MinWindSpeed })
	maxWindSpeed := mapWeatherValue(ws, func(w Weather) float64 { return w.MaxWindSpeed })
	temperatures := mapWeatherValue(ws, func(w Weather) float64 { return w.Temperature })
	gases := mapWeatherValue(ws, func(w Weather) float64 { return w.Gas })
	relativeHumidities := mapWeatherValue(ws, func(w Weather) float64 { return w.RelativeHumidity })
	pressures := mapWeatherValue(ws, func(w Weather) float64 { return w.Pressure })

	p := 0.1
	a := averageWeather{
		avgWindSpeed:     truncatedMean(avgWindSpeeds, p),
		minWindSpeed:     truncatedMean(minWindSpeeds, p),
		maxWindSpeed:     truncatedMean(maxWindSpeed, p),
		temperature:      truncatedMean(temperatures, p),
		gas:              truncatedMean(gases, p),
		relativeHumidity: truncatedMean(relativeHumidities, p),
		pressure:         truncatedMean(pressures, p),
	}

	return a
}
