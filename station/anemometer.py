import RPi.GPIO as GPIO
from threading import Lock, Thread
import time

class Anemometer:
    def __init__(self, circumference: float, channel: int):
        self.lock = Lock()
        self.circumference = circumference
        self.reset()
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(channel, GPIO.RISING, callback=self.hall_interrupt, bouncetime=200)


    def reset(self):
        with self.lock:
            self.readings = [None] * 100
            self.reading_pointer = 0
            self.last_time = None

    @property
    def speed(self):
        with self.lock:
            if self.readings[self.reading_pointer] > 0:
                return self.circumference / self.readings[self.reading_pointer]
            return 0.0


    @property
    def max_speed(self):
        min_reading = float("inf")
        with self.lock:
            for reading in self.readings:
                if reading is not None and reading < min_reading:
                    min_reading = reading
        if min_reading > 0:
            return self.circumference / min_reading
        return 0.0

    
    @property
    def min_speed(self):
        max_reading = 0
        with self.lock:
            for reading in self.readings:
                if reading is not None and reading > max_reading:
                    max_reading = reading
        if max_reading > 0:
            return self.circumference / max_reading
        return 0.0


    @property
    def average_speed(self):
        total = 0.0
        count = 0.0
        with self.lock:
            for reading in self.readings:
                if reading is not None:
                    total += reading
                    count += 1.0
        if count > 0:
            avg = total / count
            if avg > 0:
                return self.circumference / avg
        return 0.0


    def hall_interrupt(self, _):
        with self.lock:
            cur_time = time.time()
            if self.last_time is not None and cur_time - self.last_time < 30:
                self.reading_pointer = (self.reading_pointer + 1) % len(self.readings)
                self.readings[self.reading_pointer] = cur_time - self.last_time
            self.last_time = cur_time

