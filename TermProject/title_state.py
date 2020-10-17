from pico2d import*

import core
from game_state import GameState

class TitleState:
    def init(self):
        pass

    def update(self):
        if core.eh.get_key_down(SDLK_SPACE):
            core.push_state(GameState())
            return
        elif core.eh.get_key_down(SDLK_ESCAPE):
            core.pop_state()
            return

    def exit(self):
        core.renderer.clear()

    def pause(self):
        pass

    def resume(self):
        pass

if __name__ == '__main__':
    core.init(TitleState())
    core.run()