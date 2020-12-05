from pico2d import*

import core
import ui
from game_state import GameState

UI_MOVE_SPEED = 7.0

class TitleState:
    def init(self):
        self.__init()
        
    def update(self):
        
        self.start_button.update()
        self.exit_button.update()

        if self.pressed_start_button is False and self.pressed_exit_button is False:
            self.title_text.move_to(10.0, self.title_text.spr.y, UI_MOVE_SPEED)
            self.score_box.move_to(self.score_box.spr.x, 280.0, UI_MOVE_SPEED)
            self.start_button.move_to(self.start_button.spr.x, 185.0, UI_MOVE_SPEED)
            self.exit_button.move_to(self.exit_button.spr.x, 185.0, UI_MOVE_SPEED * 0.75)

            if self.start_button.is_pressed():
                self.pressed_start_button = True
            elif self.exit_button.is_pressed():
                self.pressed_exit_button = True
        else:
            self.title_text.move_to(-200.0, self.title_text.spr.y, UI_MOVE_SPEED * 1.5)
            self.score_box.move_to(self.score_box.spr.x, core.const.SCREEN_HEIGHT, UI_MOVE_SPEED * 1.5)
            self.start_button.move_to(self.start_button.spr.x, -self.start_button.spr.image.h, UI_MOVE_SPEED * 1.5)
            self.exit_button.move_to(self.exit_button.spr.x, -self.exit_button.spr.image.h, UI_MOVE_SPEED * 1.5)

            self.next_state_delay -= core.delta_time
            if self.next_state_delay <= 0.0:
                if self.pressed_start_button:
                    core.push_state(GameState())
                else:
                    core.pop_state()

                return

    def exit(self):
        pass

    def pause(self):
        core.renderer.clear()
        del self.bgm

    def resume(self):
        self.__init()

    def __init(self):
        show_cursor()

        self.bgm = load_music('./res/DST-TowerDefenseTheme.mp3')
        self.bgm.set_volume(128)
        self.bgm.repeat_play()

        background = core.Sprite('./res/background.png')
        background.camera_ignorer = True
        background.x = core.const.SCREEN_WIDTH / 2
        background.y = core.const.SCREEN_HEIGHT / 2
        core.renderer.Add(background)

        title_background = core.Sprite('./res/title_background.png')
        title_background.x = core.const.SCREEN_WIDTH / 2
        title_background.y = core.const.SCREEN_HEIGHT / 2
        core.renderer.Add(title_background)

        self.title_text = ui.UI('./res/title_text.png')
        self.title_text.spr.x = -self.title_text.spr.image.w
        self.title_text.spr.y = core.const.SCREEN_HEIGHT - 10.0
        self.title_text.spr.origin_x = 0.0
        self.title_text.spr.origin_y = 1.0

        self.score_box = ui.UI('res/score_box.png')
        self.score_box.spr.x = core.const.SCREEN_WIDTH / 2
        self.score_box.spr.y = core.const.SCREEN_HEIGHT
        self.score_box.spr.origin_y = 0.0

        self.start_button = ui.UI('res/start_idle_button.png', 'res/start_contact_button.png')
        self.start_button.spr.x = core.const.SCREEN_WIDTH / 2
        self.start_button.spr.y = -self.start_button.spr.image.h
        self.start_button.spr.origin_x = 1.0

        self.exit_button = ui.UI('res/exit_idle_button.png', 'res/exit_contact_button.png')
        self.exit_button.spr.x = core.const.SCREEN_WIDTH / 2
        self.exit_button.spr.y = -self.exit_button.spr.image.h
        self.exit_button.spr.origin_x = 0.0

        self.pressed_start_button = False
        self.pressed_exit_button = False
        self.next_state_delay = 0.5

if __name__ == '__main__':
    core.init(TitleState())
    core.run()