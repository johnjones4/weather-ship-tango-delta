from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import urllib.request
import json

DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_NONE = 2

FONT_PATH = "./Questrial-Regular.ttf"

API_PATH = "http://weather.apps.local.johnjonesfour.com/api/weather/average?range=10"


def fetch_weather():
    try:
        with urllib.request.urlopen(API_PATH) as response:
            return json.loads(response.read())
    except:
        return None


def get_direction(old_value, new_value):
    if old_value < new_value:
        return DIRECTION_UP
    elif old_value > new_value:
        return DIRECTION_DOWN
    else:
        return DIRECTION_NONE


def do_conversion(key, value):
    if key == "avg_wind_speed" or key == "min_wind_speed" or key == "max_wind_speed":
        val = value * 2.237
        return round(val, 1) if val < 10 else int(round(val))
    elif key == "temperature":
        return int(round(value * 1.8 + 32))
    elif key == "relative_humidity":
        return int(round(value))
    elif key == "pressure":
        return int(round(value / 3386 * 100))
    else:
        return int(round(value))


def convert_weather(weather):
    outcome = dict()
    for key in weather:
        outcome[key] = dict(
            value= do_conversion(key, weather[key]["current_value"]),
            direction= get_direction(weather[key]["previous_value"], weather[key]["current_value"])
        )
    return outcome


def draw_datapoint(draw, direction, value, label, x, y, width, height):
    value_height = int(height * 0.55)
    direction_height = int(value_height * 0.4)
    top_padding = int(height * 0.15)
    label_padding = int(height * 0.05)
    label_height = int(height * 0.11)

    direction_text = "↑" if direction == DIRECTION_UP else "↓" if direction == DIRECTION_DOWN else None

    value_fnt = ImageFont.truetype(FONT_PATH, value_height)
    value_width, value_height = draw.textsize(value, font=value_fnt)
    value_x = x + int((width - value_width) / 2)
    value_y = y + top_padding
    draw.text((value_x, value_y), value, font=value_fnt, fill=0)

    if direction_text:
        direction_fnt = ImageFont.truetype(FONT_PATH, direction_height)
        direction_width, direction_height = draw.textsize(direction_text, font=direction_fnt)
        direction_x = value_x - direction_width
        direction_y = value_y + int((value_height - direction_width) / 2)
        draw.text((direction_x, direction_y), direction_text, font=direction_fnt, fill=0)

    label_fnt = ImageFont.truetype(FONT_PATH, label_height)
    label_width, _ = draw.textsize(label, font=label_fnt)
    draw.text((x + int((width - label_width) / 2), y + top_padding + value_height + label_padding), label, font=label_fnt, fill=0)


def draw_weather(weather, width, height):
    subpoints = [
        (weather["max_wind_speed"]["direction"], str(weather["max_wind_speed"]["value"]), "Wind Gusts (MPH)"),
        (weather["relative_humidity"]["direction"], f"{weather['relative_humidity']['value']}%", "Humidity"),
        (weather["pressure"]["direction"], str(weather["pressure"]["value"]), "Pressure (inHg)"),
    ]

    image = Image.new("1", (width, height), 255)
    draw = ImageDraw.Draw(image)

    # draw.rectangle((0, 0, width, height), fill=1)

    subpoint_width = int(width / 3.0)
    subpoint_x = width - subpoint_width

    draw.line((subpoint_x, 0, subpoint_x, height), fill=0)

    subpoint_spacing = height / len(subpoints)
    for i, (direction, value, label) in enumerate(subpoints):
        y = int(i * subpoint_spacing)
        if i != len(subpoints) - 1:
            draw.line((subpoint_x, y + subpoint_spacing, subpoint_x + subpoint_width, y + subpoint_spacing), fill=0)
        draw_datapoint(draw, direction, value, label, subpoint_x, y, subpoint_width, subpoint_spacing)

    draw_datapoint(draw, weather["temperature"]["direction"], f"{weather['temperature']['value']}°", "Temperature (F)", 0, 0, subpoint_x, height)

    date_padding = int(height * 0.01)
    date_height = int(height * 0.04)
    date_fnt = ImageFont.truetype(FONT_PATH, date_height)
    now = datetime.now()
    date_str = now.strftime("%A, %d. %B %Y %I:%M%p")
    date_x = date_padding
    date_y = height - date_height - date_padding
    draw.text((date_x, date_y), date_str, font=date_fnt, fill=0)
    
    return image
