from core.constants import SCREEN_HEIGHT
import math
from pico2d import*

import core
from player import Player
from monster import *
from ui import UI

class GameState:
    def init(self):
        hide_cursor()
        
        self.bgm = load_music('./res/Metallic Mistress.mp3')
        self.bgm.set_volume(48)
        self.bgm.repeat_play()

        self.game_over_sound = load_music('./res/game_over.mp3')

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
        self.monster_creator_delay = 0.5
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

        self.game_over = False
        self.game_over_elapsed_time = 0.0
        self.screen_change_background = None

        self.is_pause = False

        self.resume_button = UI('./res/resume_idle_button.png', 'res/resume_contact_button.png')
        self.resume_button.spr.camera_ignorer = True
        self.resume_button.spr.x = core.const.SCREEN_WIDTH / 2
        self.resume_button.spr.y = -self.resume_button.spr.image.h
        self.resume_button.spr.origin_x = 1.0

        self.exit_button = UI('./res/ingame_exit_idle_button.png', 'res/ingame_exit_contact_button.png')
        self.exit_button.spr.camera_ignorer = True
        self.exit_button.spr.x = core.const.SCREEN_WIDTH / 2
        self.exit_button.spr.y = -self.exit_button.spr.image.h
        self.exit_button.spr.origin_x = 0.0

    def update(self):
        if self.game_over:
            self.game_over_elapsed_time += core.delta_time
            if self.game_over_elapsed_time >= 1.0:
                self.screen_change_background.alpha += core.delta_time * 0.7
                if self.screen_change_background.alpha >= 1.0:
                    core.pop_state()
            return

        if core.eh.get_key_down(SDLK_ESCAPE):
            self.is_pause = True
            show_cursor()

        if self.is_pause:
            self.resume_button.update()
            self.resume_button.move_to(self.resume_button.spr.x, SCREEN_HEIGHT * 0.5, 7.0)

            self.exit_button.update()
            self.exit_button.move_to(self.exit_button.spr.x, SCREEN_HEIGHT * 0.5, 7.0)
            
            if self.resume_button.is_pressed():
                self.is_pause = False
                hide_cursor()

            if self.exit_button.is_pressed():
                self.game_over = True
                self.__create_screen_change_background()
            
            return
        else:
            self.resume_button.move_to(self.resume_button.spr.x, -self.resume_button.spr.image.h, 15.0)
            self.exit_button.move_to(self.exit_button.spr.x, -self.exit_button.spr.image.h, 15.0)
            
        view_dir_x = self.zoom_point.x + core.camera.x - self.player.spr.x
        view_dir_y = self.zoom_point.y + core.camera.y - self.player.spr.y
        view_dis = math.sqrt(view_dir_x ** 2 + view_dir_y ** 2)

        if view_dis != 0.0:
            view_dir_x /= view_dis
            view_dir_y /= view_dis

        self.player.update(view_dir_x, view_dir_y, self.monsters)
        player_half_w = self.player.collision_box_w * 0.5
        player_half_h = self.player.collision_box_h * 0.5
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
                continue
            
            if mob.creator and mob.spr.active > 0.0:
                mob_half_w = mob.collision_box_w * 0.5
                mob_half_h = mob.collision_box_h * 0.5
                mob_left = mob.spr.x - mob_half_w
                mob_right = mob.spr.x + mob_half_w
                mob_bottom = mob.spr.y - mob_half_h
                mob_top = mob.spr.y + mob_half_h

                if player_left <= mob_right and player_right >= mob_left and player_bottom <= mob_top and player_top >= mob_bottom:
                    if self.player.spr.alpha >= 1.0:
                        self.player.hit()

                        # 게임이 종료되는지 확인합니다.
                        if self.player.hp <= 0.0:
                            self.game_over = True

                            self.bgm.stop()
                            self.game_over_sound.set_volume(127)
                            self.game_over_sound.play()

                            self.__create_screen_change_background()
                            return

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
        self.score += 2.0 * core.delta_time

        if self.view_score < self.score:
            self.view_score = min(int(self.view_score + 120.0 * core.delta_time), self.score)
            self.score_text.text = 'score: ' + str(int(self.view_score))

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

    def __create_screen_change_background(self):
        self.screen_change_background = core.Sprite('./res/screen_change_background.png')
        self.screen_change_background.camera_ignorer = True
        self.screen_change_background.x = core.const.SCREEN_WIDTH / 2
        self.screen_change_background.y = core.const.SCREEN_HEIGHT / 2
        self.screen_change_background.alpha = 0.0
        core.renderer.Add(self.screen_change_background)

if __name__ == '__main__':
    core.init(GameState())
    core.run()