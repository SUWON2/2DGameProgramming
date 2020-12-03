import random
import core
from particle import Particle

class Monster:
    SPR_PATH = './res/monster_3_0.png'
    HIT_PARTICLE0_PATH = './res/mob_hit_particle_0.png'
    HIT_PARTICLE1_PATH = './res/mob_hit_particle_1.png'
    PARTICLE_MAX = 10

    def __init__(self):
        self.spr = core.Sprite(self.SPR_PATH)
        core.renderer.Add(self.spr)

        self.hp = 100
        self.collision_box_w = 48
        self.collision_box_h = 48

        self.hit0_particles = [Particle(self.HIT_PARTICLE0_PATH, 1, 1) for i in range(self.PARTICLE_MAX)]
        self.hit1_particles = [Particle(self.HIT_PARTICLE1_PATH, 1, 1) for i in range(self.PARTICLE_MAX)]
        self.piece_particles = [Particle(self.SPR_PATH, 1, 2) for i in range(self.PARTICLE_MAX)]
        self.particle_index = 0

    def update(self):
        for i in range(self.PARTICLE_MAX):
            self.hit0_particles[i].update()
            self.hit1_particles[i].update()
            self.piece_particles[i].update()

        self.spr.scaleX = min(1.0, self.spr.scaleX + 3.0 * core.delta_time)
        self.spr.scaleY = self.spr.scaleX

    def hit(self, bullet_dir_x, bullet_dir_y):
        self.hp -= 1
        if self.hp <= 0:
            self.spr.active = False

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
