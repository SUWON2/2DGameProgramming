import math

import core
from core.sprite import Sprite

VELOCITY = 3500.0

class Bullet:
    RESOURCES = [ './res/Bullet_0.png', './res/Bullet_1.png' ]

    def __init__(self, x, y, angle, kind):
        self.spr = Sprite(self.RESOURCES[kind])
        self.spr.x = x
        self.spr.y = y
        self.spr.angle = angle
        core.renderer.Add(self.spr)

        self.dx = math.cos(math.radians(angle))
        self.dy = math.sin(math.radians(angle))

        # 총알의 초기 위치를 지정합니다.
        offset = (self.spr.image.w) * 0.15
        self.spr.x += self.dx * offset
        self.spr.y += self.dy * offset

    def __del__(self):
        pass

    def update(self):
        self.spr.x += self.dx * VELOCITY * core.delta_time
        self.spr.y += self.dy * VELOCITY * core.delta_time