from pico2d import *

import core.cache_image

class Sprite:
    def __init__(self, image_path = None):
        self.x = 0.0
        self.y = 0.0
        self.scaleX = 1.0
        self.scaleY = 1.0
        self.origin_x = 0.5
        self.origin_y = 0.5
        self.angle = 0.0
        self.alpha = 1.0
        self.active = True
        self.image = None
        self.camera_ignorer = False
        
        if image_path:
            self.set_image(image_path)

    def __del__(self):
        pass

    def set_image(self, image_path):
        self.image = core.cache_image.load(image_path)