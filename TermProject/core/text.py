from pico2d import *

import core.cache_font

class Text:
    def __init__(self, font_path = None, font_size = None):
        self.text = ''
        self.x = 0.0
        self.y = 0.0
        self.origin_x = 0.5
        self.origin_y = 0.5
        self.color_r = 255
        self.color_g = 255
        self.color_b = 255
        self.active = True
        self.ttf = None

        if font_path:
            assert font_size != None, '사이즈를 등록해 주세요'
            self.ttf = core.cache_font.load(font_path, font_size)

    def set_font(self, font_path, size):
        self.ttf = core.cache_font.load(font_path, size)