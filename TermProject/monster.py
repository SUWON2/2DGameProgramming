from random import random
import core
from particle import Particle

class Monster:
    HIT_PARTICLE0_RES = './res/mob_hit_particle_0.png'
    HIT_PARTICLE1_RES = './res/mob_hit_particle_1.png'
    HIT_PARTICLE_MAX = 5

    def __init__(self):
        self.spr = core.Sprite('./res/monster_3_0.png')
        core.renderer.Add(self.spr)

        self.hp = 100
        self.collision_box_w = 48
        self.collision_box_h = 48

        self.hit0_particles = [Particle(self.HIT_PARTICLE0_RES, 1, 1) for i in range(self.HIT_PARTICLE_MAX)]
        self.hit1_particles = [Particle(self.HIT_PARTICLE1_RES, 1, 1) for i in range(self.HIT_PARTICLE_MAX)]
        self.hit_particle_index = 0

    def update(self):
        for i in self.hit0_particles:
            i.update()

        for i in self.hit1_particles:
            i.update()

        self.spr.scaleX = min(1.0, self.spr.scaleX + 3.0 * core.delta_time)
        self.spr.scaleY = self.spr.scaleX

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.spr.active = False

        hit0_particle = self.hit0_particles[self.hit_particle_index]
        hit0_particle.init(self.spr.x, self.spr.y, 0.15, 7.0)

        hit1_particle = self.hit1_particles[self.hit_particle_index]
        hit1_particle.init(self.spr.x, self.spr.y, 0.15, 7.0)

        self.hit_particle_index += 1
        if self.hit_particle_index >= self.HIT_PARTICLE_MAX:
            self.hit_particle_index = 0

        self.spr.scaleX = 0.7
        self.spr.scaleY = self.spr.scaleX
