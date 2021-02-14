from app.widgets.widget import Widget

class LocalRadarWidget(Widget):
    def __init__(self, *args, **kwargs):
        kwargs["title"] = "Local Radar"
        super(LocalRadarWidget, self).__init__(*args, **kwargs)
        self.radar_image = kwargs.get("config")["radar_image"]

    def generate_content(self, image, x, y, width, height):
        url = f"https://radar.weather.gov/ridge/lite/{self.radar_image}.png"
        self.paint_image_from_url(url, image, x, y, width, height)
