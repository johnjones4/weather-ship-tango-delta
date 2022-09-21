package main

import (
	"fmt"
	"time"
)

func main() {
	connect()
	go runHttpServer()
	fmt.Println("HTTP server up")
	lastStatus := true
	lastStatusTime := time.Now()
	for {
		down, err := isStationDown()
		if err != nil {
			fmt.Println(err)
		} else if down != lastStatus || lastStatusTime.Before(time.Now().Add(-24*time.Hour)) {
			fmt.Printf("Station is up: %t\n", !down)
		}
		lastStatus = down
		time.Sleep(time.Minute * 60)
	}
}
