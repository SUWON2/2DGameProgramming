from pico2d import *
import random

import core
from bullet import Bullet
from monster import Monster
from particle import Particle

ACC_VELOCITY = 100.0
DEC_VELOCITY = 60.0
MAX_VELOCITY = 600.0
MAX_ATTACK_DELAY = 0.15

class Player:
    BULLET_MAX_COUNT = 20

    def __init__(self):
        self.hit_sound = load_wav('./res/boom.wav')
        self.hit_sound.set_volume(48)

        self.spr = core.Sprite('./res/player.png')
        core.renderer.Add(self.spr)

        self.hp = 5
        self.hp_sprs = []
        for i in range(self.hp):
            hp_spr = core.Sprite('./res/circle_hp_' + str(i) + '.png')
            hp_spr.active = False
            self.hp_sprs.append(hp_spr)
            core.renderer.Add(hp_spr)

        self.hp_sprs[self.hp - 1].active = True

        self.skill = core.Sprite('./res/skill.png')
        self.skill.active = False
        core.renderer.Add(self.skill)

        self.collision_box_w = 32
        self.collision_box_h = 32
        
        self.speed_x = 0.0
        self.speed_y = 0.0

        self.attack_delay = 0.0
        self.bullet_index = 0
        self.bullet_kind = 0
        self.bullets = [Bullet(self.bullet_kind) for i in range(0, self.BULLET_MAX_COUNT)]

        self.skill_guage = 0.0
        self.skill_view_guage = 0.0
        self.dash_guage = 0.0
        self.dash_view_guage = 0.0

        self.bullet_particles = []
        self.bullet_particles.append(Particle('./res/bullet_t_0.png', 1, 1))
        self.bullet_particles.append(Particle('./res/bullet_t_1.png', 1, 1))
        self.bullet_particles.append(Particle('./res/bullet_t_2.png', 1, 1))
        self.bullet_particle_index = 0;

    def __del__(self):
        for i in range(5):
            core.renderer.remove(self.hp_sprs[i])

        core.renderer.remove(self.skill)
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

        self.dash_guage = min(self.dash_guage + core.delta_time * 15.0, 100.0)

        # 총알 발사를 처리합니다.
        if core.eh.get_mouse_button(core.eh.LBUTTON) and self.attack_delay <= 0.0:
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

        # 스킬을 처리합니다.
        if self.skill.active:
            MAX_SIZE = 80.0
            self.skill.scaleX = min(self.skill.scaleX + core.delta_time * 200.0, MAX_SIZE)
            self.skill.scaleY = self.skill.scaleX

            for mob in monsters:
                if mob.spr.active:
                    mob.hit(view_dir_x, view_dir_y)

            if self.skill.scaleX >= MAX_SIZE:
                self.skill.active = False
                self.skill_guage = 0.0
                self.skill_view_guage = 0.0
        elif self.skill_guage >= 100.0:
            self.explode()

        # hp를 표시합니다.
        if self.hp >= 0:
            hp_spr = self.hp_sprs[self.hp - 1]
            hp_spr.x = self.spr.x
            hp_spr.y = self.spr.y

            hp_spr.angle -= core.delta_time * 150.0
            if hp_spr.angle <= 0.0:
                hp_spr.angle = 360.0
        
        self.spr.alpha = min(1.0, self.spr.alpha + core.delta_time * 0.3)

    def explode(self):
        self.skill.active = True
        self.skill.x = self.spr.x
        self.skill.y = self.spr.y
        self.skill.scaleX = 1.0
        self.skill.scaleY = 1.0
        self.skill.angle = self.spr.angle
        core.camera.shake(10.0, 0.5)

    def hit(self):
        if self.hp <= 0.0:
            return

        self.hp -= 1
        self.hp_sprs[self.hp].active = False

        if self.hp > 0:
            hp_spr = self.hp_sprs[self.hp - 1]
            hp_spr.active = True
            hp_spr.x = self.spr.x
            hp_spr.y = self.spr.y

        self.spr.alpha = 0.2
        self.hit_sound.play()
        core.camera.shake(5.0, 0.5)