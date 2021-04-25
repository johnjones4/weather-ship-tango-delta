package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"
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
			sendSMS(down)
		}
		lastStatus = down
		time.Sleep(time.Minute * 5)
	}
}

func sendSMS(down bool) {
	var message string
	if down {
		message = "Weather station is offline"
	} else {
		message = "Weather station is online"
	}

	accountSid := os.Getenv("TWILIO_SID")
	authToken := os.Getenv("TWILIO_AUTH_TOKEN")

	urlStr := fmt.Sprintf("https://api.twilio.com/2010-04-01/Accounts/%s/Messages.json", accountSid)

	msgData := url.Values{}
	msgData.Set("To", os.Getenv("TWILIO_NUMBER_TO"))
	msgData.Set("From", os.Getenv("TWILIO_NUMBER_FROM"))
	msgData.Set("Body", message)
	msgDataReader := *strings.NewReader(msgData.Encode())

	client := &http.Client{}
	req, _ := http.NewRequest("POST", urlStr, &msgDataReader)
	req.SetBasicAuth(accountSid, authToken)
	req.Header.Add("Accept", "application/json")
	req.Header.Add("Content-Type", "application/x-www-form-urlencoded")

	resp, _ := client.Do(req)
	if resp.StatusCode >= 200 && resp.StatusCode < 300 {
		var data map[string]interface{}
		decoder := json.NewDecoder(resp.Body)
		err := decoder.Decode(&data)
		if err == nil {
			fmt.Println(data["sid"])
		}
	} else {
		fmt.Println(resp.Status)
	}
}
