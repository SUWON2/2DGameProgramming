from pico2d import *

fonts = {}

def load(font_path, size):
    global fonts

    if font_path in fonts:
        return fonts[font_path]

    font = load_font(font_path, size)
    fonts[font_path] = font
    return font

def unload(font_path):
    global fonts

    if font_path in fonts:
        del fonts[font_path]

def clear():
    global fonts
    fonts.clear()