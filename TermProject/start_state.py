from pico2d import*

import core
from title_state import TitleState

class StartState:
    def init(self):
        self.logo = core.sprite.Sprite('res/kpu_logo.png')
        self.logo.x = core.constants.SCREEN_WIDTH / 2
        self.logo.y = core.constants.SCREEN_HEIGHT / 2
        core.renderer.Add(self.logo)

        self.elapsed_time = 0.0

    def update(self):
        self.elapsed_time += core.delta_time
        if self.elapsed_time >= 1.0:
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