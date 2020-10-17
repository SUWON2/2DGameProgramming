from pico2d import*

import core

class GameState:
    def init(self):
        self.player = core.sprite.Sprite('./res/ball21x21.png')
        self.player.x = core.constants.SCREEN_WIDTH / 2
        self.player.y = core.constants.SCREEN_HEIGHT / 2
        core.renderer.Add(self.player)

    def update(self):
        if core.events_handler.get_key_down(SDLK_ESCAPE):
            core.pop_state()
            return

    def exit(self):
        core.renderer.clear()

    def pause(self):
        pass

    def resume(self):
        pass

if __name__ == '__main__':
    core.init(GameState())
    core.run()