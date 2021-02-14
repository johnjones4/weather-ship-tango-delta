from app.widgets.widget import Widget
import urllib.request
import io
from PIL import Image

class USRadarWidget(Widget):
    def __init__(self, *args, **kwargs):
        kwargs["title"] = "US Radar"
        super(USRadarWidget, self).__init__(*args, **kwargs)

    def generate_content(self, image, x, y, width, height):
        self.paint_image_from_url("https://radar.weather.gov/Conus/RadarImg/latest.gif", image, x, y, width, height)
