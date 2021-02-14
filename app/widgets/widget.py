from PIL import Image, ImageDraw, ImageFont
import traceback
import urllib.request
import io

FONT_TYPE_NORMAL = "normal"
FONT_TYPE_BOLD = "bold"

class Widget:
    def __init__(self, *args, **kwargs):
        self.title = kwargs.get("title", "Widget")
        self.inset = kwargs.get("inset", 0)
        self.font_size = kwargs.get("font_size", 0)
        self.font_path = kwargs.get("font_path")
        self.bold_font_path = kwargs.get("bold_font_path")
        self.position = kwargs.get("config")["position"]

    def generate(self, mode, width, height, color):
        image = Image.new(mode, (width, height), color=color)
        drawable = ImageDraw.Draw(image)
        drawable.rectangle(((0,0), (width-1,height-1)), fill=None, outline=0, width=1)
        try:
            self.generate_content(image, self.inset, self.inset + self.font_size, width - (self.inset * 2), height - (self.inset * 2) - self.font_size)
        except Exception as e:
            print(traceback.format_exc())
            self.generate_error_content(image, self.inset, self.inset + self.font_size, width - (self.inset * 2), height - (self.inset * 2) - self.font_size, str(e))
        drawable.text((self.inset, self.inset), self.title, fill=0, font=self.get_font(self.font_size, FONT_TYPE_BOLD))
        return image

    def generate_content(self, image, x, y, width, height):
        return

    def generate_error_content(self, image, x, y, width, height, error_str):
        self.draw_basic_lines_of_text(error_str, image, x, y, width, height)

    def get_font(self, ofsize=None, font_type=FONT_TYPE_NORMAL):
        if ofsize is None:
            ofsize = self.font_size
        if font_type == FONT_TYPE_NORMAL:
            return ImageFont.truetype(self.font_path, ofsize)
        elif font_type == FONT_TYPE_BOLD:
            return ImageFont.truetype(self.bold_font_path, ofsize)
        else:
            return None

    def get_position(self):
        return (self.position["row"], self.position["col"], self.position["row_span"], self.position["col_span"])

    def text_to_render_array(self, draw, text_array, max_width):
        lines = []
        for (font_size, line_height, font, text) in text_array:
            for text_line in text.split("\n"):
                current_line = []
                for word in text_line.split(" "):
                    current_line_joined = " ".join(current_line)
                    (width, _) = draw.multiline_textsize(current_line_joined + " " + word, font=font)
                    if width > max_width:
                        lines.append((font_size, line_height, font, current_line_joined))
                        current_line = [word]
                    else:
                        current_line.append(word)
                if len(current_line) > 0:
                    lines.append((font_size, line_height, font, " ".join(current_line)))
        return lines

    def draw_basic_lines_of_text(self, text, image, x, y, width, height):
        self.draw_lines_of_text([(self.font_size, int(self.font_size * 1.25), self.get_font(self.font_size), text)], image, x, y, width, height)

    def draw_lines_of_text(self, text_array, image, x, y, width, height):
        last_y = y
        drawable = ImageDraw.Draw(image)
        text_lines = self.text_to_render_array(drawable, text_array, width)
        for (font_size, line_height, font, line) in text_lines:
            last_y += line_height
            if last_y + font_size > y + height:
                return
            drawable.multiline_text((x,last_y), line, font=font, fill=0)
            
        return last_y

    def paint_image_from_url(self, url, image, x, y, width, height):
        with urllib.request.urlopen(url) as url_req:
            f = io.BytesIO(url_req.read())
            img = Image.open(f).convert(image.mode, colors=255)
            image_width, image_height = img.size
            widget_width = width - x
            widget_height = height - y
            widget_ratio = widget_width / widget_height
            image_ratio = image_width / image_height
            if widget_ratio < image_ratio:
                paste_x = x
                paste_width = widget_width
                paste_height = int((paste_width * image_height) / image_width)
                paste_y = int(y + (widget_height - paste_height) / 2) + self.font_size
            else:
                paste_y = y + self.font_size
                paste_height = widget_height
                paste_width = int((paste_height * image_width) / image_height)
                paste_x = int(x + (widget_width - paste_width) / 2)
            image.paste(img.resize((paste_width, paste_height)), (paste_x, paste_y))
