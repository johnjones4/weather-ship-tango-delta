import yaml
from app.dashboard import Dashboard
from app.widgets.local_radar_widget import LocalRadarWidget
from app.widgets.us_radar_widget import USRadarWidget
from app.widgets.alerts_widget import AlertsWidget
from app.widgets.forecast_widget import ForecastWidget
from app.widgets.temperature_widget import TemperatureWidget
from app.widgets.wind_widget import WindWidget

class DashboardConfig:
    def __init__(self, path, args):
        self.path = path
        self.load_config()
        if len(args) > 1:
            self.config["output"] = args[1]

    def load_config(self):
        with open(self.path, 'r') as file:
            self.config = yaml.load(file.read(), Loader=yaml.SafeLoader)

    def get(self, key):
        if key not in self.config:
            raise Exception("Key \"%s\" not in config!" % (key))
        return self.config[key]

    def generate_dashboard(self):
        text_global_config = self.get("text")
        font_size = text_global_config["font_size"]
        font_path = text_global_config["font_path"]
        bold_font_path = text_global_config["bold_font_path"]
        dashboard_config = self.get("dashboard")
        return Dashboard(
            dashboard_config["width"],
            dashboard_config["height"],
            dashboard_config["rows"],
            dashboard_config["cols"],
            dashboard_config["gutter"],
            dashboard_config["show_status"],
            font_size,
            font_path,
            bold_font_path
        )

    def generate_widgets(self):
        widget_global_config = self.get("widget")
        text_global_config = self.get("text")
        font_size = text_global_config["font_size"]
        padding = widget_global_config["padding"]
        font_path = text_global_config["font_path"]
        bold_font_path = text_global_config["bold_font_path"]
        widgets = self.get("widgets")
        widget_instances = []
        for widget_config in widgets:
            widget = self.init_widget(widget_config["type"], font_size, font_path, bold_font_path, padding, widget_config)
            widget_instances.append(widget)
        return widget_instances

    def init_widget(self, widget_type, font_size, font_path, bold_font_path, padding, config):
        args = []
        kwargs = dict(
            font_size=font_size,
            font_path=font_path,
            bold_font_path=bold_font_path,
            inset=padding,
            config=config
        )
        if widget_type == "local_radar":
            return LocalRadarWidget(*args, **kwargs)
        elif widget_type == "us_radar":
            return USRadarWidget(*args, **kwargs)
        elif widget_type == "alerts":
            return AlertsWidget(*args, **kwargs)
        elif widget_type == "forecast":
            return ForecastWidget(*args, **kwargs)
        elif widget_type == "temperature":
            return TemperatureWidget(*args, **kwargs)
        elif widget_type == "wind":
            return WindWidget(*args, **kwargs)
