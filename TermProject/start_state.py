from pico2d import*

import core
from title_state import TitleState

class StartState:
    def init(self):
        self.background = core.sprite.Sprite('./res/start_state/background_piece.png')
        self.background.scaleX = core.const.SCREEN_WIDTH / 10
        self.background.scaleY = core.const.SCREEN_HEIGHT / 10
        self.background.origin_x = 0.0
        self.background.origin_y = 0.0
        core.renderer.Add(self.background)

        self.logo = core.sprite.Sprite('./res/start_state/kpu_logo.png')
        self.logo.x = core.const.SCREEN_WIDTH / 2
        self.logo.y = core.const.SCREEN_HEIGHT / 2
        self.logo.alpha = 0.0
        core.renderer.Add(self.logo)

        self.alpha_up = True

    def update(self):
        if self.alpha_up:
            self.logo.alpha += 0.5 * core.delta_time
            if self.logo.alpha >= 0.9:
                self.alpha_up = False
        else:
            self.logo.alpha -= 0.5 * core.delta_time
            if self.logo.alpha < 0.0:
                core.change_state(TitleState())

    def exit(self):
        core.renderer.clear()

    def pause(self):
        pass

    def resume(self):
        pass

if __name__ == '__main__':
    core.init(StartState())
    core.run()