from weatherstation.render import convert_weather, draw_weather
from lib.waveshare_epd import epd7in5
import time

if __name__ == "__main__":
    while True:
        raw_weather = dict(
            max_wind_speed=dict(
                current_value=0,
                previous_value=-1
            ),
            temperature=dict(
                current_value=0,
                previous_value=1
            ),
            gas=dict(
                current_value=0,
                previous_value=0
            ),
            relative_humidity=dict(
                current_value=0,
                previous_value=-1
            ),
            pressure=dict(
                current_value=0,
                previous_value=1
            ),
        )
        epd = epd7in5.EPD()
        weather = convert_weather(raw_weather)
        image = draw_weather(weather, epd.width, epd.height)    
        epd.init()
        epd.Clear()
        epd.display(epd.getbuffer(image))

        time.sleep(60)
