from pico2d import *
import random

import core
from bullet import Bullet
from monster import Monster
from particle import Particle

ACC_VELOCITY = 80.0
DEC_VELOCITY = 120.0
MAX_VELOCITY = 500.0
MAX_ATTACK_DELAY = 0.15

class Player:
    BULLET_MAX_COUNT = 20

    def __init__(self):
        self.spr = core.Sprite('./res/player.png')
        core.renderer.Add(self.spr)
        
        self.speed_x = 0.0
        self.speed_y = 0.0

        self.attack_delay = 0.0

        self.bullet_index = 0
        self.bullet_kind = 0
        self.bullets = [Bullet(self.bullet_kind) for i in range(0, self.BULLET_MAX_COUNT)]

        self.bullet_particles = []
        self.bullet_particles.append(Particle('./res/bullet_t_0.png', 1, 1))
        self.bullet_particles.append(Particle('./res/bullet_t_1.png', 1, 1))
        self.bullet_particles.append(Particle('./res/bullet_t_2.png', 1, 1))
        self.bullet_particle_index = 0;

    def __del__(self):
        core.renderer.remove(self.spr)

    def update(self, view_dir_x, view_dir_y, monsters):
        move_dir_x = core.eh.get_key(SDLK_d) - core.eh.get_key(SDLK_a)
        move_dir_y = core.eh.get_key(SDLK_w) - core.eh.get_key(SDLK_s)

        if move_dir_x != 0.0:
            if move_dir_x > 0.0:
                self.speed_x = min(self.speed_x + ACC_VELOCITY, MAX_VELOCITY)
            else:
                self.speed_x = max(self.speed_x - ACC_VELOCITY, -MAX_VELOCITY)
        else:
            if self.speed_x > 0.0:
                self.speed_x = max(self.speed_x - DEC_VELOCITY, 0.0)
            else:
                self.speed_x = min(self.speed_x + DEC_VELOCITY, 0.0)

        if move_dir_y != 0.0:
            if move_dir_y > 0.0:
                self.speed_y = min(self.speed_y + ACC_VELOCITY, MAX_VELOCITY)
            else:
                self.speed_y = max(self.speed_y - ACC_VELOCITY, -MAX_VELOCITY)
        else:
            if self.speed_y > 0.0:
                self.speed_y = max(self.speed_y - DEC_VELOCITY, 0.0)
            else:
                self.speed_y = min(self.speed_y + DEC_VELOCITY, 0.0)

        final_speed_x = self.speed_x
        final_speed_y = self.speed_y

        if final_speed_x != 0.0 and final_speed_y != 0.0:
            speed_size = math.sqrt(final_speed_x ** 2 + final_speed_y ** 2)
            final_speed_x *= abs(final_speed_x) / speed_size
            final_speed_y *= abs(final_speed_y) / speed_size

        to_x = self.spr.x + final_speed_x * core.delta_time
        to_y = self.spr.y + final_speed_y * core.delta_time

        if -core.const.BOUNDARY_HALF_W < to_x and to_x < core.const.BOUNDARY_HALF_W:
            self.spr.x = to_x

        if -core.const.BOUNDARY_HALF_H < to_y and to_y < core.const.BOUNDARY_HALF_H:
            self.spr.y = to_y

        self.spr.angle = math.degrees(math.atan2(view_dir_y, view_dir_x)) - 90.0

        if self.attack_delay >= 0.0:
            self.attack_delay -= core.delta_time

        if core.eh.get_mouse_button(core.eh.LBUTTON) and self.attack_delay <= 0.0:
            bullet = None

            # 총알을 재활용합니다.
            self.bullets[self.bullet_index].init(self.spr.x, self.spr.y, self.spr.angle + random.randrange(87, 94), monsters)
            self.bullet_index += 1
            if self.bullet_index >= self.BULLET_MAX_COUNT:
                self.bullet_index = 0

            self.attack_delay = MAX_ATTACK_DELAY
            self.bullet_kind = not self.bullet_kind

            # 총알 이펙트를 출력합니다.
            bullet_particle = self.bullet_particles[self.bullet_particle_index]
            bullet_particle.min_random_x = -10.0
            bullet_particle.max_random_x = 10.0
            bullet_particle.min_random_y = -10.0
            bullet_particle.max_random_y = 10.0
            bullet_particle.move_dir_x = -view_dir_x
            bullet_particle.move_dir_y = -view_dir_y
            bullet_particle.move_velocity = random.uniform(700.0, 900.0)
            bullet_particle.move_dec_velocity = 45.0
            bullet_particle.max_angle = random.randrange(-360, 360)
            bullet_particle.angle_speed = abs(bullet_particle.max_angle) * 250.0 / 90.0
            bullet_particle.min_scale = 1.0
            bullet_particle.alpha_speed = 3.0
            bullet_particle.init(self.spr.x, self.spr.y, 0.4)

            self.bullet_particle_index += 1
            if self.bullet_particle_index >= len(self.bullet_particles):
                self.bullet_particle_index = 0

            core.camera.shake(3.0, 0.05)

        for i in self.bullets:
            i.update()

        for i in self.bullet_particles:
            i.update()