package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"
	"time"
)

func getStatus(w http.ResponseWriter, req *http.Request) {
	fmt.Fprintf(w, "{\"status\": \"ok\"}")
}

func getInfo(w http.ResponseWriter, req *http.Request) {
	now := time.Now().UTC()
	then := now.Add(time.Hour * -24 * 7)
	downtime, err := getDowntimeStats(then, now)
	if err != nil {
		errorResponse(w, err)
		return
	}
	reboots, err := getRebootCount(then, now)
	if err != nil {
		errorResponse(w, err)
		return
	}
	info := ServerInfo{downtime, reboots}
	jsonResponse(w, info)
}

func getWeatherAverage(w http.ResponseWriter, req *http.Request) {
	irange, err := strconv.Atoi(req.URL.Query()["range"][0])
	if err != nil {
		errorResponse(w, err)
		return
	}
	mrange := time.Minute * time.Duration(irange) * -1
	now := time.Now().UTC()
	start1 := now.Add(mrange)
	end1 := now
	start2 := now.Add(mrange * 2)
	end2 := now.Add(mrange)
	currentSegment, err := getWeatherInRange(start1, end1)
	if err != nil {
		errorResponse(w, err)
		return
	}
	current := determineAverageWeather(currentSegment)
	comparisonSegment, err := getWeatherInRange(start2, end2)
	if err != nil {
		errorResponse(w, err)
		return
	}
	previous := determineAverageWeather(comparisonSegment)
	resp := AverageWeatherResponse{
		AvgWindSpeed:     AverageWeatherValue{current.avgWindSpeed, previous.avgWindSpeed},
		MinWindSpeed:     AverageWeatherValue{current.minWindSpeed, previous.minWindSpeed},
		MaxWindSpeed:     AverageWeatherValue{current.maxWindSpeed, previous.maxWindSpeed},
		Temperature:      AverageWeatherValue{current.temperature, previous.temperature},
		Gas:              AverageWeatherValue{current.gas, previous.gas},
		RelativeHumidity: AverageWeatherValue{current.relativeHumidity, previous.relativeHumidity},
		Pressure:         AverageWeatherValue{current.pressure, previous.pressure},
	}
	jsonResponse(w, resp)
}

func insertNewWeather(w http.ResponseWriter, req *http.Request) {
	if req.Method != "POST" {
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("NOT FOUND"))
		return
	}
	body, err := ioutil.ReadAll(req.Body)
	if err != nil {
		errorResponse(w, err)
		return
	}
	var weather Weather
	err = json.Unmarshal(body, &weather)
	if err != nil {
		errorResponse(w, err)
		return
	}
	weather.Timestamp = time.Now().UTC()
	err = insertWeatherData(weather)
	if err != nil {
		errorResponse(w, err)
		return
	}
	jsonResponse(w, weather)
}

func runHttpServer() {
	mux := &http.ServeMux{}

	mux.HandleFunc("/api", getStatus)
	mux.HandleFunc("/api/info", getInfo)
	mux.HandleFunc("/api/weather/average", getWeatherAverage)
	mux.HandleFunc("/api/weather", insertNewWeather)

	var handler http.Handler = mux
	handler = logRequestHandler(handler)

	srv := &http.Server{
		Addr:    os.Getenv("HTTP_SERVER"),
		Handler: handler,
	}
	srv.ListenAndServe()
}
