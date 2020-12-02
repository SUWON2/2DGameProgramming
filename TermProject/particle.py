import random

import core

class Particle:
    def __init__(self, image_path, min_count, max_count):
        assert(min_count >= 1 and min_count < max_count, '최소 개수는 1 이상, 최대 개수는 최소 개수 이상으로 설정해야 됩니다.')

        self.pieces = []
        for i in range(max_count):
            piece = core.Sprite(image_path)
            piece.active = False
            core.renderer.Add(piece)
            self.pieces.append(piece)

        self.min_count = min_count
        self.max_count = max_count
        self.cur_count = 0

        self.life_time = 0.0
        self.scale_speed = 0.0

    def init(self, x, y, life_time, scale_speed):
        self.cur_count = random.randrange(self.min_count, self.max_count + 1)
        for i in range(self.cur_count):
            piece = self.pieces[i]
            piece.x = x + random.uniform(-20.0, 20.0)
            piece.y = y + random.uniform(-20.0, 20.0)
            piece.scaleX = 0.0
            piece.scaleY = 0.0
            piece.active = True

        self.life_time = life_time
        self.scale_speed = scale_speed

    def update(self):
        if self.life_time <= 0.0:
            return

        for i in range(self.cur_count):
            piece = self.pieces[i]
            piece.scaleX = min(1.0, piece.scaleX + self.scale_speed * core.delta_time)
            piece.scaleY = piece.scaleX

        self.life_time -= core.delta_time
        if self.life_time <= 0.0:
             for i in range(self.cur_count):
                 piece = self.pieces[i]
                 piece.active = False