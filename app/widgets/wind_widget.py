from app.widgets.widget import Widget
from app.widgets.observation_widget import ObservationWidget
import io
from PIL import Image, ImageDraw
import requests

class WindWidget(ObservationWidget):
    def __init__(self, *args, **kwargs):
        kwargs["title"] = "Wind"
        super(WindWidget, self).__init__(*args, **kwargs)

    def generate_content(self, image, x, y, width, height):
        observations = self.get_current_observations()
        if not observations:
            self.draw_basic_lines_of_text("No Wind", image, x, y, width, height)
            return
        self.circle_padding = self.font_size * 2
        c_height = height - self.font_size
        if width > c_height:
            self.circle_width = c_height - (self.circle_padding * 2)
            self.circle_x = int(x + self.circle_padding + ((width - (self.circle_width + (self.circle_padding * 2))) / 2))
            self.circle_y = y + self.circle_padding
        else:
            self.circle_width = width - (self.circle_padding * 2)
            self.circle_x = x + self.circle_padding
            self.circle_y = int(y + self.circle_padding + ((c_height - (self.circle_width + (self.circle_padding * 2))) / 2))
        self.arrow_size = int(self.circle_width * 0.65)
        self.draw_arrow(image, x, y, width, height, observations["windDirection"]["value"])
        self.draw_compass(image, x, y, width, height)
        self.draw_speed(image, x, y, width, height, observations["windSpeed"]["value"])
        return

    def draw_speed(self, image, x, y, width, height, speed):
        speed = f"{round(speed * 2.23694, 2)} mph"
        drawable = ImageDraw.Draw(image)
        (t_width, t_height) = drawable.textsize(
            speed,
            font=self.get_font(),
        )
        drawable.text(
            (
                x + (width / 2) - (t_width / 2),
                y + height - t_height
            ),
            speed,
            fill=1,
            font=self.get_font()
        )

    def draw_arrow(self, image, x, y, width, height, deg):
        arrow_image = Image.new(image.mode, (self.arrow_size, self.arrow_size), color=255)
        drawable = ImageDraw.Draw(arrow_image)
        drawable.polygon(
            [
                (int(self.arrow_size / 2), 0),
                (self.arrow_size, int(self.arrow_size * 0.9)),
                (int(self.arrow_size / 2), int(self.arrow_size * 0.7)),
                (0, int(self.arrow_size * 0.9))
            ],
            outline=None,
            fill=1
        )
        arrow_aligned = arrow_image.rotate(
            360 - int(deg),
            expand=True,
            fillcolor="white"
        )
        image.paste(
            arrow_aligned,
            box=(
                self.circle_x + int((self.circle_width - arrow_aligned.width) / 2),
                self.circle_y + int((self.circle_width - arrow_aligned.height) / 2)
            )
        )
                
    def draw_compass(self, image, x, y, width, height):
        drawable = ImageDraw.Draw(image)

        # Circle
        drawable.ellipse(
            [
                (self.circle_x, self.circle_y),
                (self.circle_x + self.circle_width, self.circle_y + self.circle_width)
            ],
            fill=None,
            outline=1,
            width=1
        )

        # Compass
        (t_width, _) = drawable.textsize(
            "N",
            font=self.get_font(),
        )
        drawable.text(
            (
                self.circle_x + (self.circle_width / 2) - (t_width / 2),
                self.circle_y - (self.circle_padding * 0.75)
            ),
            "N",
            fill=1,
            font=self.get_font()
        )

        (t_width, _) = drawable.textsize(
            "S",
            font=self.get_font(),
        )
        drawable.text(
            (
                self.circle_x + (self.circle_width / 2) - (t_width / 2),
                self.circle_y + (self.circle_width)
            ),
            "S",
            fill=1,
            font=self.get_font()
        )

        (t_width, t_height) = drawable.textsize(
            "W",
            font=self.get_font(),
        )
        drawable.text(
            (
                self.circle_x - t_width - (self.circle_padding * 0.25),
                self.circle_y + (self.circle_width / 2) - (t_height / 2)
            ),
            "W",
            fill=1,
            font=self.get_font()
        )

        drawable.text(
            (
                self.circle_x + self.circle_width + (self.circle_padding * 0.25),
                self.circle_y + (self.circle_width / 2) - (t_height / 2)
            ),
            "E",
            fill=1,
            font=self.get_font()
        )
