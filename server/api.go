package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/gorilla/mux"
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

func insertNewWeather(w http.ResponseWriter, req *http.Request) {
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

	err = publishWeather(weather)
	if err != nil {
		errorResponse(w, err)
		return
	}

	jsonResponse(w, weather)
}

func getWeather(w http.ResponseWriter, req *http.Request) {
	var (
		start time.Time
		end   time.Time
	)

	startStr := req.URL.Query().Get("start")
	if startStr != "" {
		i, err := strconv.Atoi(startStr)
		if err != nil {
			errorResponse(w, err)
			return
		}
		start = time.Unix(int64(i), 0).UTC()
	} else {
		start = time.Now().UTC().Add(time.Hour * -24)
	}

	endStr := req.URL.Query().Get("end")
	if endStr != "" {
		i, err := strconv.Atoi(endStr)
		if err != nil {
			errorResponse(w, err)
			return
		}
		end = time.Unix(int64(i), 0).UTC()
	} else {
		end = time.Now().UTC()
	}

	weather, err := getWeatherInRange(start, end)
	if err != nil {
		errorResponse(w, err)
		return
	}

	weather = eliminateOutliers(weather)

	jsonResponse(w, weather)
}

func runHttpServer() {
	mux := mux.NewRouter()

	mux.HandleFunc("/api", getStatus).Methods("GET")
	mux.HandleFunc("/api/info", getInfo).Methods("GET")
	mux.HandleFunc("/api/weather", insertNewWeather).Methods("POST")
	mux.HandleFunc("/api/weather", getWeather).Methods("GET")

	var handler http.Handler = mux
	handler = logRequestHandler(handler)

	srv := &http.Server{
		Addr:    os.Getenv("HTTP_SERVER"),
		Handler: handler,
	}
	srv.ListenAndServe()
}
