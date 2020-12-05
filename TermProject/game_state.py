import math
from pico2d import*

import core
from player import Player
from monster import *

class GameState:
    def init(self):
        hide_cursor()
        
        self.bgm = load_music('./res/Metallic Mistress.mp3')
        self.bgm.set_volume(48)
        self.bgm.repeat_play()

        background = core.Sprite('./res/background.png')
        background.camera_ignorer = True
        background.x = core.const.SCREEN_WIDTH / 2
        background.y = core.const.SCREEN_HEIGHT / 2
        core.renderer.Add(background)

        boundary = core.Sprite('./res/boundary.png')
        core.renderer.Add(boundary)

        self.player = Player()

        self.monsters = []
        self.monster_kinds = [ Monster1, Monster2, Monster3, Monster4 ]
        self.monster_max_count = 20
        self.monster_creator_delay = 2.0
        self.monster_creator_elapsed_time = 0.0

        self.zoom_point = core.Sprite('./res/zoom_point.png')
        self.zoom_point.camera_ignorer = True
        core.renderer.Add(self.zoom_point)

        self.zoom_outer = core.Sprite('./res/zoom_outer.png')
        self.zoom_outer.camera_ignorer = True
        core.renderer.Add(self.zoom_outer)

        self.score = 0
        self.view_score = 0
        self.score_text = core.Text('./res/Kontakt.ttf', 36)
        self.score_text.x = 550.0
        self.score_text.y = core.const.SCREEN_HEIGHT - 60.0
        self.score_text.text = 'SCORE: 0'
        core.renderer.Add(self.score_text)
        
        self.skill_guage_back_spr = core.Sprite('./res/guage_back.png')
        self.skill_guage_back_spr.camera_ignorer = True
        self.skill_guage_back_spr.x = core.const.SCREEN_WIDTH * 0.5
        self.skill_guage_back_spr.y = 25.0
        core.renderer.Add(self.skill_guage_back_spr)

        self.skill_guage_spr = core.Sprite('./res/skill_guage.png')
        self.skill_guage_spr.camera_ignorer = True
        self.skill_guage_spr.x = self.skill_guage_back_spr.x
        self.skill_guage_spr.y = self.skill_guage_back_spr.y
        self.skill_guage_spr.origin_y = self.skill_guage_back_spr.origin_y
        self.skill_guage_spr.scaleX = 0.0
        core.renderer.Add(self.skill_guage_spr)

        self.dash_guage_back_spr = core.Sprite('./res/guage_back.png')
        self.dash_guage_back_spr.camera_ignorer = True
        self.dash_guage_back_spr.x = core.const.SCREEN_WIDTH * 0.5
        self.dash_guage_back_spr.y = 45.0
        core.renderer.Add(self.dash_guage_back_spr)

        self.dash_guage_spr = core.Sprite('./res/dash_guage.png')
        self.dash_guage_spr.camera_ignorer = True
        self.dash_guage_spr.x = self.dash_guage_back_spr.x
        self.dash_guage_spr.y = self.dash_guage_back_spr.y
        self.dash_guage_spr.origin_y = self.dash_guage_back_spr.origin_y
        self.dash_guage_spr.scaleX = 0.0
        core.renderer.Add(self.dash_guage_spr)

    def update(self):
        if core.eh.get_key_down(SDLK_ESCAPE):
            core.pop_state()
            return

        # if core.eh.get_key_down(SDLK_SPACE):
        #     if self.player.spr.alpha >= 1.0:
        #         self.player.hit()

        view_dir_x = self.zoom_point.x + core.camera.x - self.player.spr.x
        view_dir_y = self.zoom_point.y + core.camera.y - self.player.spr.y
        view_dis = math.sqrt(view_dir_x ** 2 + view_dir_y ** 2)

        if view_dis != 0.0:
            view_dir_x /= view_dis
            view_dir_y /= view_dis

        self.player.update(view_dir_x, view_dir_y, self.monsters)
        player_half_w = self.player.spr.image.w * 0.5
        player_half_h = self.player.spr.image.h * 0.5
        player_left = self.player.spr.x - player_half_w
        player_right = self.player.spr.x + player_half_w
        player_bottom = self.player.spr.y - player_half_h
        player_top = self.player.spr.y + player_half_h


        # 몬스터를 업데이트하고, 플레이어와 충돌 처리를 확인합니다
        for mob in self.monsters:
                if mob.update(self.player.spr.x, self.player.spr.y) == False:
                    self.score += mob.score
                    self.player.skill_guage = min(self.player.skill_guage + random.uniform(5.0, 7.0), 100.0)
                
                if mob.dead_time >= 2.0:
                    self.monsters.remove(mob)
                else:
                    mob_half_w = mob.collision_box_w * 0.5
                    mob_half_h = mob.collision_box_h * 0.5
                    mob_left = mob.spr.x - mob_half_w
                    mob_right = mob.spr.x + mob_half_w
                    mob_bottom = mob.spr.y - mob_half_h
                    mob_top = mob.spr.y + mob_half_h

                    if player_left <= mob_right and player_right >= mob_left and player_bottom <= mob_top and player_top >= mob_bottom:
                        if self.player.spr.alpha >= 1.0:
                            self.player.hit()

        self.__update_score()
        self.__update_guage()
        self.__update_zoom(view_dir_x, view_dir_y, view_dis)
        self.__update_camera()

        # 몬스터를 주기적으로 생성합니다.
        self.monster_creator_elapsed_time = min(self.monster_creator_elapsed_time + core.delta_time, self.monster_creator_delay)
        if self.monster_creator_elapsed_time >= self.monster_creator_delay:
            if len(self.monsters) < self.monster_max_count:
                x = random.uniform(-core.const.BOUNDARY_HALF_W + 10.0, core.const.BOUNDARY_HALF_W - 10.0)
                y = random.uniform(-core.const.BOUNDARY_HALF_H + 10.0, core.const.BOUNDARY_HALF_H - 10.0)
                monster_kind = self.monster_kinds[random.randrange(0, len(self.monster_kinds))]

                mob = monster_kind()
                mob.init(x, y)
                self.monsters.append(mob)

                self.monster_creator_elapsed_time = 0.0

    def exit(self):
        core.renderer.clear()

    def pause(self):
        pass

    def resume(self):
        pass

    def __update_zoom(self, view_dir_x, view_dir_y, zoom_dis):
        self.zoom_point.x = core.eh.mouse_pos[0]
        self.zoom_point.y = core.eh.mouse_pos[1]
        self.zoom_outer.x = core.eh.mouse_pos[0]
        self.zoom_outer.y = core.eh.mouse_pos[1]

        zoom_scale = min(max(1.0, zoom_dis / 300.0), 1.5)
        self.zoom_outer.scaleX = zoom_scale
        self.zoom_outer.scaleY = zoom_scale

    def __update_score(self):
        if self.view_score < self.score:
            self.view_score = min(int(self.view_score + 120.0 * core.delta_time), self.score)
            self.score_text.text = 'score: ' + str(self.view_score)

    def __update_guage(self):
        self.player.skill_view_guage += (self.player.skill_guage - self.player.skill_view_guage) * 5.0 * core.delta_time + 0.025
        self.skill_guage_spr.scaleX = self.player.skill_view_guage / 100.0
        self.skill_guage_spr.x = self.skill_guage_back_spr.x - self.skill_guage_spr.image.w * (1 - self.skill_guage_spr.scaleX) * 0.5

        self.player.dash_view_guage += (self.player.dash_guage - self.player.dash_view_guage) * 5.0 * core.delta_time + 0.025
        self.dash_guage_spr.scaleX = self.player.dash_view_guage / 100.0
        self.dash_guage_spr.x = self.dash_guage_back_spr.x - self.dash_guage_spr.image.w * (1 - self.dash_guage_spr.scaleX) * 0.5

    def __update_camera(self):
        CAMERA_VELOCITY = 8
        target_x = self.player.spr.x - core.const.SCREEN_WIDTH / 2
        target_y = self.player.spr.y - core.const.SCREEN_HEIGHT / 2
        core.camera.x += (target_x - core.camera.x) * CAMERA_VELOCITY * core.delta_time
        core.camera.y += (target_y - core.camera.y) * CAMERA_VELOCITY * core.delta_time

if __name__ == '__main__':
    core.init(GameState())
    core.run()