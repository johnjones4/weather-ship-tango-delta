from app.widgets.widget import FONT_TYPE_BOLD
from app.widgets.observation_widget import ObservationWidget
import io
from PIL import Image, ImageDraw
import requests

TEMP_MAX = 110
TEMP_MIN = -20

class TemperatureWidget(ObservationWidget):
    def __init__(self, *args, **kwargs):
        kwargs["title"] = "Temperature"
        super(TemperatureWidget, self).__init__(*args, **kwargs)

    def generate_content(self, image, x, y, width, height):
        observations = self.get_current_observations()
        if not observations:
            self.draw_basic_lines_of_text("No Current Conditions", image, x, y, width, height)
            return
        self.thermometer_width = int(width / 3)
        self.thermometer_height = int(height * 0.8)
        self.thermometer_x = int((width - self.thermometer_width) / 3)
        self.thermometer_y = int((height - self.thermometer_height) / 1.5)
        self.base_width = int(self.thermometer_width * 1.5)
        self.draw_thermometer(image, x, y, width, height)
        self.draw_scale(image, x, y, width, height)
        self.draw_temps(image, x, y, width, height, observations)

    def draw_temps(self, image, x, y, width, height, observations):
        drawable = ImageDraw.Draw(image)
        f = round((observations["temperature"]["value"] * (9 / 5)) + 32, 2)
        (t_width, _) = drawable.textsize(f"{f}°", font=self.get_font())
        temp_y = self.get_y_for_temp(f)
        drawable.text(
            (self.thermometer_x + int(self.thermometer_width / 2) - int(t_width / 2), int(temp_y - self.font_size * 1.2)),
            f"{f}°",
            fill=0,
            font=self.get_font()
        )
        drawable.rectangle(
            [
                (self.thermometer_x, temp_y),
                (self.thermometer_x + self.thermometer_width, self.thermometer_y + self.thermometer_height - (self.base_width * 0.7)),
            ],
            fill="black",
            width=1
        )
        for (label, prop) in [("Dew Point", "dewpoint"), ("Heat Index", "heatIndex")]:
            if prop in observations and observations[prop]["value"]:
                f = (observations[prop]["value"] * (9 / 5)) + 32 
                temp_y = self.get_y_for_temp(f)
                drawable.line(
                    [
                        (self.thermometer_x, temp_y),
                        (self.thermometer_x + self.thermometer_width + 10, temp_y),
                    ],
                    fill="black",
                    width=1
                )
                text_x = self.thermometer_x + self.thermometer_width + 15
                text_y = temp_y - int(self.font_size)
                drawable.text(
                    (text_x, int(text_y + self.font_size * 1.2)),
                    f"{round(f,2)}°",
                    fill=0,
                    font=self.get_font()
                )
                drawable.text(
                    (text_x, text_y),
                    label + ":",
                    fill=0,
                    font=self.get_font()
                )

    def get_y_for_temp(self, temp):
        y_range = int((self.thermometer_width / 2) + (self.thermometer_height - (self.thermometer_width / 2) - self.base_width))
        t_range = TEMP_MAX - TEMP_MIN
        return self.thermometer_y + int(y_range * ((TEMP_MAX - temp) / t_range))

    def draw_scale(self, image, x, y, width, height):
        drawable = ImageDraw.Draw(image)
        temps = [TEMP_MAX, 32, -10]
        for temp in temps:
            temp_y = self.get_y_for_temp(temp) + self.font_size
            (t_width, _) = drawable.textsize(f"{temp}°", font=self.get_font())
            drawable.text(
                (x + self.thermometer_x - int(t_width * 1.25), temp_y),
                f"{temp}°",
                fill=0,
                font=self.get_font()
            )

    def draw_thermometer(self, image, x, y, width, height):
        drawable = ImageDraw.Draw(image)
        
        outset = int((self.base_width - self.thermometer_width) / 2)
        
        drawable.arc(
            [
                (self.thermometer_x, self.thermometer_y),
                (self.thermometer_x + self.thermometer_width, self.thermometer_y + self.thermometer_width)
            ],
            -180,
            0,
            fill=None,
            width=1
        )

        drawable.line(
            [
                (self.thermometer_x, self.thermometer_y + int(self.thermometer_width / 2)),
                (self.thermometer_x, self.thermometer_y + self.thermometer_height - (self.base_width * 0.86)),
            ],
            fill="black",
            width=1
        )

        drawable.line(
            [
                (self.thermometer_x + self.thermometer_width, self.thermometer_y + int(self.thermometer_width / 2)),
                (self.thermometer_x + self.thermometer_width, self.thermometer_y + self.thermometer_height - (self.base_width * 0.86)),
            ],
            fill="black",
            width=1
        )

        drawable.ellipse(
            [
                (self.thermometer_x - outset, self.thermometer_y + self.thermometer_height - self.base_width),
                (self.thermometer_x - outset + self.base_width, self.thermometer_y + self.thermometer_height)
            ],
            fill="black",
            width=0
        )

