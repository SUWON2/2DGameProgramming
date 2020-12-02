import core

class Monster:
    def __init__(self):
        self.spr = core.Sprite('./res/monster_3_0.png')
        core.renderer.Add(self.spr)

        self.collision_box_w = 48
        self.collision_box_h = 48

        self.hp = 100

    def update(self):
        pass

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.spr.active = False
