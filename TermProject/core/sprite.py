from pico2d import *

import core.cache_image as cimage

class Sprite:
    def __init__(self, image_path = None):
        self.x = 0.0
        self.y = 0.0
        self.scaleX = 1.0
        self.scaleY = 1.0
        self.image = None
        
        if image_path:
            self.set_image(image_path)

    def __del__(self):
        pass

    def set_image(self, image_path):
        self.image = cimage.load(image_path)