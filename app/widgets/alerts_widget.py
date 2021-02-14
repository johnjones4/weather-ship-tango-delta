from app.widgets.widget import Widget
import io
from PIL import Image
import requests

class AlertsWidget(Widget):
    def __init__(self, *args, **kwargs):
        kwargs["title"] = "Alerts"
        super(AlertsWidget, self).__init__(*args, **kwargs)
        self.point = kwargs.get("config")["point"]

    def generate_content(self, image, x, y, width, height):
        info = requests.get(f"https://api.weather.gov/alerts/active?point={self.point}").json()
        if "features" not in info or not info["features"]:
            self.draw_basic_lines_of_text("No Alerts", image, x, y, width, height)
            return
        alerts = "\n".join(["• " + message["properties"]["headline"] for message in info["features"]])
        self.draw_basic_lines_of_text(alerts, image, x, y, width, height)

