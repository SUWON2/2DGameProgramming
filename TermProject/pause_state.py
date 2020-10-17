from pico2d import*

import core
from game_state import GameState

class PauseState:
    def init(self):
        pass

    def update(self):
        pass

    def exit(self):
        pass
    
    def pause(self):
        pass

    def resume(self):
        pass

if __name__ == '__main__':
    core.run(PauseState())