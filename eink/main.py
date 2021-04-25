from weatherstation.render import render
from lib.waveshare_epd import epd7in5
import time

if __name__ == "__main__":
    while True:
        image = render(epd.width, epd.height)
        if image:
            epd = epd7in5.EPD()
            epd.init()
            epd.Clear()
            epd.display(epd.getbuffer(image))
        time.sleep(60)
