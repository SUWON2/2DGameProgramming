import math

from pico2d import *
import core
from core.sprite import Sprite

VELOCITY = 3500.0

class Bullet:
    RESOURCES = [ './res/Bullet_0.png', './res/Bullet_1.png' ]

    def __init__(self, kind):
        self.spr = Sprite(self.RESOURCES[kind])
        self.spr.active = False
        core.renderer.Add(self.spr)

        self.shoot_sound = load_wav('./res/shoot_sound.wav')
        self.shoot_sound.set_volume(128)

        self.burst_sound = load_wav('./res/bullet_sound.wav')
        self.burst_sound.set_volume(8)
        
    def __del__(self):
        core.renderer.remove(self.spr)

    def init(self, x, y, angle, monsters):
        self.spr.active = True
        self.spr.angle = angle
        self.spr.alpha = 0.0
        self.dir_x = math.cos(math.radians(angle))
        self.dir_y = math.sin(math.radians(angle))

        # 총알의 초기 위치를 지정합니다.
        offset = (self.spr.image.w) * 0.15
        self.spr.x = x + self.dir_x * offset
        self.spr.y = y + self.dir_y * offset

        # 목표 몬스터를 찾습니다.
        self.target_mob = None
        mob_dis_sq_min = 999999.0
        for mob in monsters:
            if mob.spr.active == False:
                continue

            mob_half_w = mob.collision_box_w * 0.5
            mob_half_h = mob.collision_box_h * 0.5
            mob_left = mob.spr.x - mob_half_w
            mob_right = mob.spr.x + mob_half_w
            mob_bottom = mob.spr.y - mob_half_h
            mob_top = mob.spr.y + mob_half_h

            # 총알 위치를 기준으로 사분면을 구성하여 절대 충돌되지 않는 몬스터는 무시합니다.
            if self.spr.angle >= 0.0:
                if mob_top < self.spr.y:
                    continue

                # 1사 분면
                if self.spr.angle <= 90.0:
                    if mob_right < self.spr.x:
                        continue
                # 2사 분면
                else:
                    if mob_left > self.spr.x:
                        continue
            else:
                if mob_bottom > self.spr.y:
                    continue

                # 3사 분면
                if self.spr.angle <= -90:
                    if mob_left > self.spr.x:
                        continue
                # 4사 분면
                else:
                    if mob_right < self.spr.x:
                        continue

            dis_x = mob.spr.x - self.spr.x
            dis_y = mob.spr.y - self.spr.y
            dis_sq = dis_x * dis_x + dis_y * dis_y

            # 레이 캐스팅에 충돌하는 가장 가까운 몬스터를 찾습니다.
            if mob_dis_sq_min >= dis_sq and self.__is_monster_collided_by_ray_casting(mob_left, mob_right, mob_bottom, mob_top, self.dir_y / self.dir_x, self.dir_x / self.dir_y):
                self.target_mob = mob
                mob_dis_sq_min = dis_sq

        self.shoot_sound.play()

    def update(self):
        if self.spr.active == False:
            return

        self.spr.alpha = min(1.0, self.spr.alpha + core.delta_time * 7.0)
        self.spr.x += self.dir_x * VELOCITY * core.delta_time
        self.spr.y += self.dir_y * VELOCITY * core.delta_time

        # 화면에 벗어난 경우 비활성화 시킵니다.
        if self.spr.x <= -core.const.BOUNDARY_HALF_W or self.spr.x >= core.const.BOUNDARY_HALF_W or self.spr.y <= -core.const.BOUNDARY_HALF_H or self.spr.y >= core.const.BOUNDARY_HALF_H:
            self.spr.active = False
            return

        if self.target_mob != None:
            dis_x = self.target_mob.spr.x - self.spr.x
            dis_y = self.target_mob.spr.y - self.spr.y
            dis_sq = dis_x * dis_x + dis_y * dis_y

            # 타겟 몬스터에 도달한 경우 비활성화 시킵니다
            if dis_sq <= 2000.0:
                self.spr.active = False
                self.target_mob.hit(self.dir_x, self.dir_y)
                self.burst_sound.play()

    def __is_monster_collided_by_ray_casting(self, mob_left, mob_right, mob_bottom, mob_top, slope_x, slope_y):
        # 왼쪽 변에 충돌했는지 검사합니다.
        point = slope_x * (mob_left - self.spr.x) + self.spr.y
        if mob_bottom <= point and point <= mob_top:
            return True

        # 오른쪽 변에 충돌했는지 검사합니다.
        point = slope_x * (mob_right - self.spr.x) + self.spr.y
        if mob_bottom <= point and point <= mob_top:
            return True

        # 밑 변에 충돌했는지 검사합니다.
        point = slope_y * (mob_bottom - self.spr.y) + self.spr.x
        if mob_left <= point and point <= mob_right:
            return True

        # 윗 변에 충돌했는지 검사합니다.
        point = slope_y * (mob_top - self.spr.y) + self.spr.x
        if  mob_left <= point and point <= mob_right:
            return True

        return False