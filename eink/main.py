from weatherstation.render import convert_weather, draw_weather, fetch_weather
from lib.waveshare_epd import epd7in5
import time

if __name__ == "__main__":
    while True:
        raw_weather = fetch_weather()
        if raw_weather:
            epd = epd7in5.EPD()
            weather = convert_weather(raw_weather)
            image = draw_weather(weather, epd.width, epd.height)    
            epd.init()
            epd.Clear()
            epd.display(epd.getbuffer(image))
        time.sleep(60)
