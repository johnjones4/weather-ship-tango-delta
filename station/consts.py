from dotenv import load_dotenv
load_dotenv()
import os

API_URL = os.getenv("API_URL")
TEMPERATURE_OFFSET = 0
ANEMOMETER_PIN = 17
ANEMOMETER_CIRCUMFERENCE = 80.0 / 1000.0
SLEEP_TIME = 60
