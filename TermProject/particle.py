import math
import random

import core

class Particle:
    def __init__(self, image_path, min_count, max_count):
        assert min_count >= 1 and min_count <= max_count, '최소 개수는 1 이상, 최대 개수는 최소 개수 이상으로 설정해야 됩니다.'

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

        self.min_random_x = 0.0
        self.max_random_x = 0.0
        self.min_random_y = 0.0
        self.max_random_y = 0.0

        self.move_dir_x = 0.0
        self.move_dir_y = 0.0
        self.move_velocity = 0.0
        self.move_dec_velocity = 0.0

        self.min_angle = 0.0
        self.max_angle = 0.0
        self.angle_speed = 0.0

        self.min_scale = 0.0
        self.max_scale = 1.0
        self.scale_speed = 0.0

        self.min_alpha = 0.0
        self.max_alpha = 1.0
        self.alpha_speed = 0.0

    def __del__(self):
        for piece in self.pieces:
            core.renderer.remove(piece)

    def init(self, x, y, life_time):
        self.cur_count = random.randrange(self.min_count, self.max_count + 1)
        for i in range(self.cur_count):
            piece = self.pieces[i]
            piece.x = x + random.uniform(self.min_random_x, self.max_random_x)
            piece.y = y + random.uniform(self.min_random_y, self.max_random_y)
            piece.angle = self.min_angle
            piece.scaleX = self.min_scale
            piece.scaleY = self.min_scale
            piece.alpha = self.min_alpha
            piece.active = True

        self.life_time = life_time

    def update(self):
        if self.life_time <= 0.0:
            return

        for i in range(self.cur_count):
            piece = self.pieces[i]
            piece.x += self.move_dir_x * self.move_velocity * core.delta_time
            piece.y += self.move_dir_y * self.move_velocity * core.delta_time
            piece.scaleX = min(self.max_scale, piece.scaleX + self.scale_speed * core.delta_time)
            piece.scaleY = piece.scaleX
            piece.angle = min(self.max_angle, piece.angle + self.angle_speed * core.delta_time)
            piece.alpha = min(self.max_alpha, piece.alpha + self.alpha_speed * core.delta_time)

        self.move_velocity = max(0.0, self.move_velocity - self.move_dec_velocity)

        self.life_time -= core.delta_time
        if self.life_time <= 0.0:
             for i in range(self.cur_count):
                 piece = self.pieces[i]
                 piece.active = False