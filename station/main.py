import time
import board
from busio import I2C
import adafruit_bme680
import RPi.GPIO as GPIO
import consts
from anemometer import Anemometer
import requests
import json

def take_reading():
    try:
        data = dict(
            timestamp= int(time.time()),
            avg_wind_speed= ANEMOMETER.average_speed,
            min_wind_speed= ANEMOMETER.min_speed,
            max_wind_speed= ANEMOMETER.max_speed,
            temperature= BME680.temperature + consts.TEMPERATURE_OFFSET,
            gas= BME680.gas,
            relative_humidity= BME680.relative_humidity,
            pressure= BME680.pressure
        )
        requests.post(f"{consts.API_URL}/api/weather", data=json.dumps(data), headers={
            "Content-type": "application/json"
        })
        print(data)
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    
    ANEMOMETER = Anemometer(consts.ANEMOMETER_CIRCUMFERENCE, consts.ANEMOMETER_PIN)
    I2C_INSTANCE = I2C(board.SCL, board.SDA)
    BME680 = adafruit_bme680.Adafruit_BME680_I2C(I2C_INSTANCE, debug=False)

    while True:
        start = time.time()
        take_reading()
        ANEMOMETER.reset()
        finish = time.time()
        time.sleep(consts.SLEEP_TIME - (finish - start))
