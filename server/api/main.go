package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"

	"github.com/google/uuid"
)

func main() {
	connect()
	go runHttpServer()
	fmt.Println("HTTP server up")
	lastStatus := true
	for {
		down, err := isStationDown()
		if err != nil {
			fmt.Println(err)
		} else if down != lastStatus {
			err := sendAlert(os.Getenv("UPSTREAM_URL"), down)
			if err != nil {
				fmt.Println(err)
			}
		}
		lastStatus = down
		time.Sleep(time.Minute * 60)
	}
}

func sendAlert(host string, down bool) error {
	payloadMap := map[string]interface{}{
		"eventVendorType": "weather-station",
		"eventVendorID":   uuid.NewString(),
		"vendorInfo": map[string]interface{}{
			"up": !down,
		},
		"alerts":   []interface{}{},
		"isNormal": !down,
	}

	payloadBytes, err := json.Marshal(payloadMap)
	if err != nil {
		return err
	}

	resp, err := http.Post(fmt.Sprintf("http://%s/api/event", host), "application/json", io.NopCloser(bytes.NewBuffer(payloadBytes)))
	if err != nil {
		return err
	}

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("http error: %d/%s", resp.StatusCode, resp.Status)
	}

	return nil
}
