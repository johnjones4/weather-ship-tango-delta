package main

import (
	"encoding/json"
	"fmt"
	"net/http"
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

func determineAverageWeather(ws []Weather) averageWeather {
	a := averageWeather{0, 0, 0, 0, 0, 0, 0}
	for _, w := range ws {
		a.avgWindSpeed += w.AvgWindSpeed
		a.minWindSpeed += w.MinWindSpeed
		a.maxWindSpeed += w.MaxWindSpeed
		a.temperature += w.Temperature
		a.gas += w.Gas
		a.relativeHumidity += w.RelativeHumidity
		a.pressure += w.Pressure
	}
	t := float64(len(ws))
	a.avgWindSpeed = a.avgWindSpeed / t
	a.minWindSpeed = a.minWindSpeed / t
	a.maxWindSpeed = a.maxWindSpeed / t
	a.temperature = a.temperature / t
	a.gas += a.gas / t
	a.relativeHumidity += a.relativeHumidity / t
	a.pressure += a.pressure / t
	return a
}
