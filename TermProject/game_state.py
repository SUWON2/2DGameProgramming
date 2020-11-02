import math
from pico2d import*

import core

# HACK: player 클래스를 따로 마련하자
ACC_VELOCITY = 50.0
DEC_VELOCITY = 120.0
MAX_VELOCITY = 500.0

class GameState:
    def init(self):
        hide_cursor()

        background = core.sprite.Sprite('./res/background.png')
        background.camera_ignorer = True
        background.x = core.const.SCREEN_WIDTH / 2
        background.y = core.const.SCREEN_HEIGHT / 2
        core.renderer.Add(background)

        boundary = core.sprite.Sprite('./res/boundary.png')
        core.renderer.Add(boundary)

        self.player = core.sprite.Sprite('./res/player.png')
        core.renderer.Add(self.player)

        self.player_speed_x = 0.0
        self.player_speed_y = 0.0

        self.zoom_point = core.sprite.Sprite('./res/zoom_point.png')
        self.zoom_point.camera_ignorer = True
        core.renderer.Add(self.zoom_point)

        self.zoom_outer = core.sprite.Sprite('./res/zoom_outer.png')
        self.zoom_outer.camera_ignorer = True
        core.renderer.Add(self.zoom_outer)

        self.zoom_scale = 0.7

    def update(self):
        if core.eh.get_key_down(SDLK_ESCAPE):
            core.pop_state()
            return

        move_dir_x = core.eh.get_key(SDLK_d) - core.eh.get_key(SDLK_a)
        move_dir_y = core.eh.get_key(SDLK_w) - core.eh.get_key(SDLK_s)

        if move_dir_x != 0.0:
            if move_dir_x > 0.0:
                self.player_speed_x = min(self.player_speed_x + ACC_VELOCITY, MAX_VELOCITY)
            else:
                self.player_speed_x = max(self.player_speed_x - ACC_VELOCITY, -MAX_VELOCITY)
        else:
            if self.player_speed_x > 0.0:
                self.player_speed_x = max(self.player_speed_x - DEC_VELOCITY, 0.0)
            else:
                self.player_speed_x = min(self.player_speed_x + DEC_VELOCITY, 0.0)

        if move_dir_y != 0.0:
            if move_dir_y > 0.0:
                self.player_speed_y = min(self.player_speed_y + ACC_VELOCITY, MAX_VELOCITY)
            else:
                self.player_speed_y = max(self.player_speed_y - ACC_VELOCITY, -MAX_VELOCITY)
        else:
            if self.player_speed_y > 0.0:
                self.player_speed_y = max(self.player_speed_y - DEC_VELOCITY, 0.0)
            else:
                self.player_speed_y = min(self.player_speed_y + DEC_VELOCITY, 0.0)

        final_speed_x = self.player_speed_x
        final_speed_y = self.player_speed_y

        if final_speed_x != 0.0 and final_speed_y != 0.0:
            speed_size = math.sqrt(final_speed_x ** 2 + final_speed_y ** 2)
            final_speed_x *= abs(final_speed_x) / speed_size
            final_speed_y *= abs(final_speed_y) / speed_size

        self.player.x += final_speed_x * core.delta_time
        self.player.y += final_speed_y * core.delta_time

        self.zoom_point.x = core.eh.mouse_pos[0]
        self.zoom_point.y = core.eh.mouse_pos[1]
        self.zoom_outer.x = core.eh.mouse_pos[0]
        self.zoom_outer.y = core.eh.mouse_pos[1]

        view_dir_x = self.zoom_point.x + core.camera.x - self.player.x
        view_dir_y = self.zoom_point.y + core.camera.y - self.player.y
        zoom_dis = math.sqrt(view_dir_x ** 2 + view_dir_y ** 2)

        self.zoom_scale = min(max(1.0, zoom_dis / 300.0), 1.5)
        self.zoom_outer.scaleX = self.zoom_scale
        self.zoom_outer.scaleY = self.zoom_scale

        if zoom_dis != 0.0:
            view_dir_x /= zoom_dis
            view_dir_y /= zoom_dis
        
        self.player.angle = math.degrees(math.atan2(view_dir_y, view_dir_x)) - 90.0

        CAMERA_VELOCITY = 8
        target_x = self.player.x - core.const.SCREEN_WIDTH / 2
        target_y = self.player.y - core.const.SCREEN_HEIGHT / 2
        core.camera.x += (target_x - core.camera.x) * CAMERA_VELOCITY * core.delta_time
        core.camera.y += (target_y - core.camera.y) * CAMERA_VELOCITY * core.delta_time

    def exit(self):
        core.renderer.clear()

    def pause(self):
        pass

    def resume(self):
        pass

if __name__ == '__main__':
    core.init(GameState())
    core.run()