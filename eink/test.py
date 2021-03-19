from weatherstation.render import convert_weather, draw_weather, fetch_weather

if __name__ == "__main__":
    raw_weather = fetch_weather()
    if raw_weather:
        weather = convert_weather(raw_weather)
        image = draw_weather(weather, 640, 384)
        image.show()
