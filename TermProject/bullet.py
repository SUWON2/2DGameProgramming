from core.sprite import Sprite
import core

VELOCITY = 2500.0

class Bullet:
    def __init__(self, x, y, dx, dy, angle):
        self.spr = core.sprite.Sprite('./res/bullet.png')
        self.spr.x = x
        self.spr.y = y
        self.spr.angle = angle
        core.renderer.Add(self.spr)

        self.dx = dx
        self.dy = dy

        # 총알의 초기 위치를 지정합니다.
        offset = (self.spr.image.w) * 0.25
        self.spr.x += self.dx * offset
        self.spr.y += self.dy * offset

    def __del__(self):
        pass

    def update(self):
        self.spr.x += self.dx * VELOCITY * core.delta_time
        self.spr.y += self.dy * VELOCITY * core.delta_time