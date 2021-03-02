from dotenv import load_dotenv
load_dotenv()
import os
import math

API_URL = os.getenv("API_URL")
TEMPERATURE_OFFSET = -5
ANEMOMETER_PIN = 17
ANEMOMETER_CIRCUMFERENCE = (80.0 / 1000.0) * 2.0 * math.pi
SLEEP_TIME = 60
