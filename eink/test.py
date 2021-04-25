from weatherstation.render import render

if __name__ == "__main__":
    image = render(640, 384)
    image.show()
