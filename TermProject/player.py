from pico2d import *
import random

import core
from bullet import Bullet
from monster import Monster

ACC_VELOCITY = 50.0
DEC_VELOCITY = 120.0
MAX_VELOCITY = 600.0
MAX_ATTACK_DELAY = 0.15

class Player:
    def __init__(self):
        self.spr = core.Sprite('./res/player.png')
        core.renderer.Add(self.spr)
        
        self.attack_sound = load_wav('./res/s_shot2.wav')
        self.attack_sound.set_volume(128)

        self.attack_sound_1 = load_wav('./res/s_shot.wav')
        self.attack_sound_1.set_volume(64)

        self.speed_x = 0.0
        self.speed_y = 0.0

        self.attack_delay = 0.0

        self.bullet_index = 0
        self.bullet_kind = 0

        self.bullets = []
        self.bullets.append(Bullet(self.bullet_kind))

    def __del__(self):
        pass

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

        self.spr.x += final_speed_x * core.delta_time
        self.spr.y += final_speed_y * core.delta_time
        self.spr.angle = math.degrees(math.atan2(view_dir_y, view_dir_x)) - 90.0

        if self.attack_delay >= 0.0:
            self.attack_delay -= core.delta_time

        if core.eh.get_mouse_button(core.eh.LBUTTON) and self.attack_delay <= 0.0:
            bullet = None

            # 총알을 재활용합니다.
            if self.bullet_index < len(self.bullets):
                bullet = self.bullets[self.bullet_index]
            else:
                self.bullet_index = 0

                bullet = self.bullets[self.bullet_index]
                if bullet.spr.active:
                    bullet = Bullet(self.bullet_kind)
                    self.bullets.append(bullet)

            bullet.init(self.spr.x, self.spr.y, self.spr.angle + random.randrange(87, 94), monsters)
            
            self.attack_sound.play()
            core.camera.shake(1.8, 0.05)

            self.attack_delay = MAX_ATTACK_DELAY
            self.bullet_kind = not self.bullet_kind
            self.bullet_index += 1

        for i in self.bullets:
            i.update()