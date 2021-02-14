from app.widgets.widget import Widget, FONT_TYPE_BOLD
import io
from PIL import Image
import requests

class ForecastWidget(Widget):
    def __init__(self, *args, **kwargs):
        kwargs["title"] = "Forecast"
        super(ForecastWidget, self).__init__(*args, **kwargs)
        self.zone_type = kwargs.get("config")["zone_type"]
        self.zone_id = kwargs.get("config")["zone_id"]

    def generate_content(self, image, x, y, width, height):
        url = f"https://api.weather.gov/zones/{self.zone_type}/{self.zone_id}/forecast"
        info = requests.get(url).json()
        print(url)
        if "properties" not in info or not info["properties"]["periods"]:
            self.draw_basic_lines_of_text("No Forecast", image, x, y, width, height)
            return
        text_array = []
        for forecast in info["properties"]["periods"]:
            text_array.append((
                self.font_size,
                int(self.font_size * 1.75),
                self.get_font(self.font_size, FONT_TYPE_BOLD),
                forecast['name'] + ": "
            ))
            text_array.append((
                self.font_size,
                int(self.font_size * 1.25),
                self.get_font(self.font_size),
                forecast['detailedForecast'].replace("\n", " ").strip()
            ))
        self.draw_lines_of_text(text_array, image, x, y, width, height)

