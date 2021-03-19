#include <WiFi.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <HTTPClient.h>
#include "Adafruit_BME680.h"
#include "secrets.h"

Adafruit_BME680 bme;

const int postDataDelay = 60000;

const int anemometerPin = 33;
const int anemometerDebounce = 200;
const int anemometerBufferSize = 100;
const double anemometerCircumference = 0.50265482457;
const unsigned long anemometerElapsedLimit = 5000;

const char* ssid = WIFI_SSID;
const char* password = WIFI_PASSWORD;
const char* postURL = POST_URL;

double anemometerBuffer[anemometerBufferSize];
int anemometerBufferPointer = 0;
unsigned long lastAnemometerSpinTime = 0;
bool lastState = false;

unsigned long lastNow = 0;
unsigned long lastPost = 0;

bool isWifiConnected() {
  return WiFi.status() == WL_CONNECTED;
}

void connectToNetwork() {
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
//    Serial.println("Establishing connection to WiFi..");
  }
 
  Serial.println("Connected to network");
 
}

void checkAnemometer(unsigned long now) {
  unsigned long elapsed = now - lastAnemometerSpinTime;
  if (elapsed >= anemometerElapsedLimit) {
    logAnemometerReading(0);
    lastAnemometerSpinTime = now;
  } else {
    int val = analogRead(anemometerPin);
    if (!lastState && val == 0 && elapsed > anemometerDebounce) {
      logAnemometerReading(elapsed);
      lastAnemometerSpinTime = now;
      lastState = true;
    } else if (lastState && val != 0) {
      lastState = false;
    }
  }
}

void logAnemometerReading(int time) {
  if (time > 0) {
    double seconds = ((double)time) / 1000.0;
    anemometerBuffer[anemometerBufferPointer] = anemometerCircumference / seconds;
  } else {
    anemometerBuffer[anemometerBufferPointer] = 0.0;
  }
  anemometerBufferPointer += 1;
  if (anemometerBufferPointer >= anemometerBufferSize) {
    anemometerBufferPointer = 0;
  }
}

void clearAnemometerBuffer() {
  for (int i = 0; i < anemometerBufferSize; i++) {
    anemometerBuffer[i] = -1;
  }
  anemometerBufferPointer = 0;
  lastAnemometerSpinTime = 0;
}

double getAverageWindSpeed() {
  double total = 0;
  double count = 0;
  for (int i = 0; i < anemometerBufferSize; i++) {
    if (anemometerBuffer[i] >= 0) {
      total += (double)anemometerBuffer[i];
      count += 1.0;
    }
  }
  if (count == 0.0) {
    return 0.0;
  }
  return (total / count);
}

double getMinWindSpeed() {
  double minSpeed = anemometerElapsedLimit + 1;
  for (int i = 0; i < anemometerBufferSize; i++) {
    if (anemometerBuffer[i] >= 0 && anemometerBuffer[i] < minSpeed) {
      minSpeed = anemometerBuffer[i];
    }
  }
  return minSpeed;
}

double getMaxWindSpeed() {
  double maxSpeed = 0;
  for (int i = 0; i < anemometerBufferSize; i++) {
    if (anemometerBuffer[i] >= 0 && anemometerBuffer[i] > maxSpeed) {
      maxSpeed = anemometerBuffer[i];
    }
  }
  return maxSpeed;
}

void logWeatherIfReady(int now) {
  if (now - lastPost >= postDataDelay) {
    double averageWindSpeed = getAverageWindSpeed();
    double maxWindSpeed = getMaxWindSpeed();
    double minWindSpeed = getMinWindSpeed();
    clearAnemometerBuffer();

    float temperature = 0;
    float pressure = 0;
    float humidity = 0;
    float gas = 0;

    if (bme.performReading()) {
      temperature = bme.temperature;
      pressure = bme.pressure / 100.0;
      humidity = bme.humidity;
      gas = bme.gas_resistance;
    }

    if (!isWifiConnected()) {
      connectToNetwork();
    }
    
    HTTPClient http;
    http.begin(postURL);
    http.addHeader("Content-Type", "application/json");
    char postData[256];
    snprintf(postData, sizeof(postData), "{\"timestamp\":null,\"avg_wind_speed\":%f,\"min_wind_speed\":%f,\"max_wind_speed\":%f,\"temperature\":%f,\"gas\":%f,\"relative_humidity\":%f,\"pressure\":%f}", averageWindSpeed, minWindSpeed, maxWindSpeed, temperature, gas, humidity, pressure);
    int httpResponseCode = http.POST(postData);
    Serial.println(postData);
    Serial.println(httpResponseCode);

    WiFi.disconnect();

    lastPost = millis();
  }
}

void setup() {
  Serial.begin(115200);

  if (!bme.begin()) {
    Serial.println(F("Could not find a valid BME680 sensor, check wiring!"));
    while (1);
  }

  // Set all values in the wind speed buffer to -1;
  clearAnemometerBuffer();

  // Set up oversampling and filter initialization
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150); // 320*C for 150 ms 
}

void loop() {
  unsigned long now = millis();
  if (lastNow > now) {
    clearAnemometerBuffer();
  }
  lastNow = now;
  
  checkAnemometer(now);

  logWeatherIfReady(now);
}
