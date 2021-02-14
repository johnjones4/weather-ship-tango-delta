from app.widgets.widget import Widget
import requests

class ObservationWidget(Widget):
    def __init__(self, *args, **kwargs):
        super(ObservationWidget, self).__init__(*args, **kwargs)
        self.zone_id = kwargs.get("config")["zone_id"]
        self.station = kwargs.get("config")["station"]

    def get_current_observations(self):
        info = requests.get(f"https://api.weather.gov/zones/forecast/{self.zone_id}/observations").json()
        if "features" not in info or not info["features"]:
            return None
        for station in info["features"]:
            if station["properties"]["station"] == f"https://api.weather.gov/stations/{self.station}":
                return station["properties"]
        return None
