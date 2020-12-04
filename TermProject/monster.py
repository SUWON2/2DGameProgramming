import math
import random

from pico2d.pico2d import load_wav
import core
from particle import Particle

class Monster:
    HIT_PARTICLE0_PATH = './res/mob_hit_particle_0.png'
    HIT_PARTICLE1_PATH = './res/mob_hit_particle_1.png'
    PARTICLE_MAX = 10

    def __init__(self, kind):
        image_path = './res/monster_' + str(kind) + '_' + str(random.randrange(0, 6)) + '.png'

        self.spr = core.Sprite(image_path)
        self.spr.active = False
        core.renderer.Add(self.spr)

        self.hp_spr = core.Sprite('./res/monster_hp.png')
        self.hp_spr.active = False
        core.renderer.Add(self.hp_spr)

        self.hp_back_spr = core.Sprite('./res/monster_hp_back.png')
        self.hp_back_spr.active = False
        core.renderer.Add(self.hp_back_spr)

        self.die_sound = load_wav('./res/boom.wav')
        self.die_sound.set_volume(32)

        self.collision_box_w = 48
        self.collision_box_h = 48

        self.creator_particle = Particle('./res/mob_creator.png', 1, 1)
        self.creator_particle.min_scale = 0.0
        self.creator_particle.max_scale = 1.0
        self.creator_particle.scale_speed = 2.0
        self.creator_particle.max_angle = 360.0 * 5
        self.creator_particle.angle_speed = 150.0
        self.creator_particle.min_alpha = 1.0

        self.hit0_particles = [Particle(self.HIT_PARTICLE0_PATH, 1, 1) for i in range(self.PARTICLE_MAX)]
        self.hit1_particles = [Particle(self.HIT_PARTICLE1_PATH, 1, 1) for i in range(self.PARTICLE_MAX)]
        self.piece_particles = [Particle(image_path, 1, 2) for i in range(self.PARTICLE_MAX)]
        self.particle_index = 0

    def __del__(self):
        core.renderer.remove(self.spr)
        core.renderer.remove(self.hp_spr)
        core.renderer.remove(self.hp_back_spr)

    def init(self, x, y):
        self.spr.x = x
        self.spr.y = y
        self.spr.active = False

        self.hp_spr.active = False
        self.hp_back_spr.active = False

        self.max_hp = 10
        self.hp = self.max_hp

        self.move_velocity = 180.0
        self.recognition_range = 120000.0
        self.aimless_dir_x = 0.0
        self.aimless_dir_y = 0.0
        self.aimless_turn_delay = 0.0

        self.creator = False
        self.score = 10

        self.creator_particle.init(self.spr.x, self.spr.y, 1.0)

    # return: 몬스터가 바로 직전에 죽은 경우 F, 그게 아닌 경우 T를 반환
    def update(self, player_x, player_y):
        # 몬스터 생성을 처리합니다.
        if self.creator == False:
            self.creator_particle.update()
            if self.creator_particle.life_time <= 0.0:
                self.spr.active = True
                self.hp_spr.active = True
                self.hp_back_spr.active = True
                self.creator = True
            else:
                return

        # 파티클을 업데이트합니다.
        for i in range(self.PARTICLE_MAX):
            self.hit0_particles[i].update()
            self.hit1_particles[i].update()
            self.piece_particles[i].update()

        if self.spr.active == False:
            return True

        # 몬스터가 죽은 경우 효과를 발생시키고 비활성화 시킵니다.
        if self.hp <= 0.0:
            self.spr.scaleX += 4.0 * core.delta_time
            self.spr.scaleY = self.spr.scaleX
            if self.spr.scaleX >= 1.5:
                self.spr.active = False
                self.hp_back_spr.active = False
                self.die_sound.play()
                core.camera.shake(7.0, 0.1)
                
                return False

            return True

        self.spr.scaleX = min(1.0, self.spr.scaleX + 3.0 * core.delta_time)
        self.spr.scaleY = self.spr.scaleX

        dis_x = player_x - self.spr.x
        dis_y = player_y - self.spr.y
        dis_sq = dis_x * dis_x + dis_y * dis_y
        final_velocity = self.move_velocity * core.delta_time

        # 일정 범위 내에 플레이어가 존재하면 따라가도록 처리합니다.
        if dis_sq <= self.recognition_range:
            dir_x = 0.0
            dir_y = 0.0
            dis = math.sqrt(dis_sq)
            if dis != 0.0:
                dir_x = dis_x / dis
                dir_y = dis_y / dis

            to_x = self.spr.x + dir_x * final_velocity
            if -core.const.BOUNDARY_HALF_W < to_x and to_x < core.const.BOUNDARY_HALF_W:
                self.spr.x = to_x
            else:
                dir_x = 0.0

            to_y = self.spr.y + dir_y * final_velocity
            if -core.const.BOUNDARY_HALF_H < to_y and to_y < core.const.BOUNDARY_HALF_H:
                self.spr.y = to_y
            else:
                dir_y = 0.0

            self.spr.angle = math.degrees(math.atan2(dir_y, dir_x))
            self.aimless_turn_delay = 0.0
        # 일정 범위 내에 플레이어가 없으면 서성이도록 처리합니다.
        else:
            to_x = 0.0
            to_y = 0.0
            self.aimless_turn_delay -= core.delta_time

            while True:
                # 이동 방향을 구합니다.
                if self.aimless_turn_delay <= 0.0:
                    if random.randrange(0, 4) < 3:
                        self.spr.angle = random.uniform(-180.0, 180.0)
                        radian = math.radians(self.spr.angle)
                        self.aimless_dir_x = math.cos(radian)
                        self.aimless_dir_y = math.sin(radian)
                    else:
                        self.aimless_dir_x = 0.0
                        self.aimless_dir_y = 0.0

                    self.aimless_turn_delay = 4.0

                to_x = self.spr.x + self.aimless_dir_x * final_velocity
                to_y = self.spr.y + self.aimless_dir_y * final_velocity

                # 화면에 벗어나는 이동 방향인 경우 새로운 이동 방향을 구합니다.
                if to_x <= -core.const.BOUNDARY_HALF_W or to_x >= core.const.BOUNDARY_HALF_W or to_y <= -core.const.BOUNDARY_HALF_H or to_y >= core.const.BOUNDARY_HALF_H:
                    self.aimless_turn_delay = 0.0
                    continue
                else:
                    break

            self.spr.x = to_x
            self.spr.y = to_y

        self.hp_back_spr.x = self.spr.x
        self.hp_back_spr.y = self.spr.y - self.spr.image.h * 0.5 - 10.0

        self.hp_spr.x = self.hp_back_spr.x - self.hp_spr.image.w * (1 - self.hp_spr.scaleX) * 0.5
        self.hp_spr.y = self.hp_back_spr.y

        return True

    def hit(self, bullet_dir_x, bullet_dir_y):
        if self.hp <= 0:
            return

        hit0_particle = self.hit0_particles[self.particle_index]
        hit0_particle.min_random_x = -20.0
        hit0_particle.max_random_x = 20.0
        hit0_particle.min_random_y = -20.0
        hit0_particle.max_random_y = 20.0
        hit0_particle.scale_speed = 7.0
        hit0_particle.min_alpha = 1.0
        hit0_particle.init(self.spr.x, self.spr.y, 0.15)

        hit1_particle = self.hit1_particles[self.particle_index]
        hit1_particle.min_random_x = -20.0
        hit1_particle.max_random_x = 20.0
        hit1_particle.min_random_y = -20.0
        hit1_particle.max_random_y = 20.0
        hit1_particle.scale_speed = 7.0;
        hit1_particle.min_alpha = 1.0
        hit1_particle.init(self.spr.x, self.spr.y, 0.15)

        piece_particle = self.piece_particles[self.particle_index]
        piece_particle.min_random_x = -50.0
        piece_particle.max_random_x = 50.0
        piece_particle.min_random_y = -50.0
        piece_particle.max_random_y = 50.0
        piece_particle.move_dir_x = bullet_dir_x
        piece_particle.move_dir_y = bullet_dir_y
        piece_particle.move_velocity = 450.0
        piece_particle.move_dec_velocity = 25.0
        piece_particle.max_angle = random.randrange(-90, 90)
        piece_particle.angle_speed = abs(piece_particle.max_angle) * 250.0 / 90.0
        piece_particle.max_scale = 0.35
        piece_particle.scale_speed = 1.0
        piece_particle.min_alpha = 1.0
        piece_particle.init(self.spr.x, self.spr.y, 0.7)

        self.particle_index += 1
        if self.particle_index >= self.PARTICLE_MAX:
            self.particle_index = 0

        self.spr.scaleX = 0.7
        self.spr.scaleY = self.spr.scaleX

        self.hp -= 1
        self.hp_spr.scaleX = self.hp / self.max_hp

class Monster1(Monster):
    def __init__(self):
        super().__init__(1)

        self.recognition_range = 200000.0

class Monster2(Monster):
    def __init__(self):
        super().__init__(2)

        self.move_velocity = 300.0
        self.score = 12

class Monster3(Monster):
    def __init__(self):
        super().__init__(3)

        self.max_hp = 20
        self.hp = self.max_hp
        self.move_velocity = 120.0
        self.score = 12

class Monster4(Monster):
    def __init__(self):
        super().__init__(4)

        self.max_hp = 15
        self.hp = self.max_hp
        self.move_velocity = 230.0
        self.recognition_range = 150000.0
        self.score = 15