from weatherstation.render import convert_weather, draw_weather

if __name__ == "__main__":
    raw_weather = dict(
        max_wind_speed=dict(
            current_value=0,
            previous_value=-1
        ),
        temperature=dict(
            current_value=0,
            previous_value=1
        ),
        gas=dict(
            current_value=0,
            previous_value=0
        ),
        relative_humidity=dict(
            current_value=0,
            previous_value=-1
        ),
        pressure=dict(
            current_value=0,
            previous_value=1
        ),
    )
    weather = convert_weather(raw_weather)
    image = draw_weather(weather, 640, 384)
    image.show()
