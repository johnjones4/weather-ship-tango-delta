from PIL import Image

DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_NONE = 2


def get_direction(old_value, new_value):
    if old_value < new_value:
        return DIRECTION_UP
    elif old_value > new_value:
        return DIRECTION_DOWN
    else:
        return DIRECTION_NONE


def do_conversion(key, value):
    if key == "wind_speed":
        return value * 2.237
    elif key == "temperature":
        return value * 1.8 + 32
    elif key == "relative_humidity":
        return value * 100
    elif key == "pressure":
        return value / 3386
    else:
        return value


def convert_weather(weather):
    outcome = dict()
    for key in weather:
        outcome[key] = dict(
            value= do_conversion(key, weather[key]["current_value"]),
            direction= get_direction(weather[key]["previous_value"], weather[key]["current_value"])
        )
    return outcome


def draw_weather(weather):
    image = Image("1", (800, 480), 1)
    draw = ImageDraw.Draw(image)
    
    return image


raw_weather = dict(
    wind_speed=dict(
        current_value=0,
        previous_value=0
    ),
    temperature=dict(
        current_value=0,
        previous_value=0
    ),
    gas=dict(
        current_value=0,
        previous_value=0
    ),
    relative_humidity=dict(
        current_value=0,
        previous_value=0
    ),
    pressure=dict(
        current_value=0,
        previous_value=0
    ),
)
weather = convert_weather(raw_weather)
draw_weather(weather)
