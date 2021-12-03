#include <WiFi.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <HTTPClient.h>
#include <esp_task_wdt.h>
#include "Adafruit_BME680.h"
#include "secrets.h"

Adafruit_BME680 bme;

#define MEASUREMENT_TIMEOUT 30
#define SLEEP_TIME 5 * 60 * 1000 * 1000
#define ANEMOMETER_PIN 33
#define ANEMOMETER_DEBOUNCE 200
#define ANEMOMETER_BUFFER_SIZE 1000
#define ANEMOMETER_CIRCUMFERENCE 0.50265482457
#define ANEMOMETER_ELAPSED_LIMIT 5000

double anemometerBuffer[ANEMOMETER_BUFFER_SIZE];
int anemometerBufferPointer = 0;
unsigned long lastAnemometerSpinTime = 0;
bool lastState = false;

void connectWifi() {
  WiFi.config(STATIC_IP, STATIC_GATEWAY, STATIC_SUBNET, STATIC_DNS); 
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  const unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Establishing connection to WiFi..");
    if (millis() - start > 60000) {
      Serial.println("WiFi timeout ... rebooting");
      ESP.restart();
    }
  }
 
  Serial.println("Connected to network");
 
}

void disconnectWifi() {
  WiFi.disconnect(true);
  Serial.println("Disconnected from network");
}

void checkAnemometer(unsigned long now) {
  unsigned long elapsed = now - lastAnemometerSpinTime;
  if (elapsed >= ANEMOMETER_ELAPSED_LIMIT) {
    logAnemometerReading(0);
    lastAnemometerSpinTime = now;
  } else {
    int val = analogRead(ANEMOMETER_PIN);
    if (!lastState && val == 0 && elapsed > ANEMOMETER_DEBOUNCE) {
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
    anemometerBuffer[anemometerBufferPointer] = ANEMOMETER_CIRCUMFERENCE / seconds;
  } else {
    anemometerBuffer[anemometerBufferPointer] = 0.0;
  }
  anemometerBufferPointer += 1;
  if (anemometerBufferPointer >= ANEMOMETER_BUFFER_SIZE) {
    anemometerBufferPointer = 0;
  }
}

void clearAnemometerBuffer() {
  for (int i = 0; i < ANEMOMETER_BUFFER_SIZE; i++) {
    anemometerBuffer[i] = -1;
  }
  anemometerBufferPointer = 0;
  lastAnemometerSpinTime = 0;
  lastState = false;
}

double getAverageWindSpeed() {
  double total = 0;
  double count = 0;
  for (int i = 0; i < ANEMOMETER_BUFFER_SIZE; i++) {
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
  double minSpeed = ANEMOMETER_ELAPSED_LIMIT + 1;
  for (int i = 0; i < ANEMOMETER_BUFFER_SIZE; i++) {
    if (anemometerBuffer[i] >= 0 && anemometerBuffer[i] < minSpeed) {
      minSpeed = anemometerBuffer[i];
    }
  }
  return minSpeed;
}

double getMaxWindSpeed() {
  double maxSpeed = 0;
  for (int i = 0; i < ANEMOMETER_BUFFER_SIZE; i++) {
    if (anemometerBuffer[i] >= 0 && anemometerBuffer[i] > maxSpeed) {
      maxSpeed = anemometerBuffer[i];
    }
  }
  return maxSpeed;
}

bool logWeather() {
  Serial.printf("Reporting data\n");
  
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
  } else {
    Serial.println("Bad sensor reading ... rebooting");
    ESP.restart();
  }


  connectWifi();
  
  HTTPClient http;
  http.begin(POST_URL);
  http.addHeader("Content-Type", "application/json");
  char postData[512];
  snprintf(postData, sizeof(postData), "{\"uptime\":%d,\"avg_wind_speed\":%f,\"min_wind_speed\":%f,\"max_wind_speed\":%f,\"temperature\":%f,\"gas\":%f,\"relative_humidity\":%f,\"pressure\":%f}", millis(), averageWindSpeed, minWindSpeed, maxWindSpeed, temperature, gas, humidity, pressure);
  int httpResponseCode = http.POST(postData);
  Serial.println(postData);
  Serial.println(httpResponseCode);
  if (httpResponseCode != 200) {
    Serial.println("Bad HTTP response code ... rebooting");
    ESP.restart();
  }

  disconnectWifi();

  return true;
}

void setup() {
  esp_task_wdt_init(90, true);
  esp_task_wdt_add(NULL);
  
  Serial.begin(115200);

  Serial.println("Starting up");

  if (!bme.begin()) {
    Serial.println(F("Could not find a valid BME680 sensor, check wiring!"));
    ESP.restart();
  }

  // Set all values in the wind speed buffer to -1;
  clearAnemometerBuffer();

  // Set up oversampling and filter initialization
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150); // 320*C for 150 ms 

  Serial.println("Ready");
}

void loop() {
  unsigned long now = millis();
  
  checkAnemometer(now);

  if (now / 1000 >= MEASUREMENT_TIMEOUT) {
    logWeather();
    esp_sleep_enable_timer_wakeup(SLEEP_TIME);
    esp_deep_sleep_start();
    clearAnemometerBuffer();
  }

  esp_task_wdt_reset();
}
