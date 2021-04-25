package main

import "fmt"

func main() {
	connect()
	go runHttpServer()
	fmt.Println("HTTP server up")
	for true {
	}
}
