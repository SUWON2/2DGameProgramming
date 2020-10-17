from pico2d import *

import core

eh = core.events_handler
renderer = core.renderer
sprite = core.sprite

player = None

def init():
    global player
    player = sprite.Sprite('./res/ball21x21.png')
    player.x = core.constants.SCREEN_WIDTH / 2
    player.y = core.constants.SCREEN_HEIGHT / 2
    renderer.Add(player)

def update():
    if eh.get_key_down(SDLK_ESCAPE):
        core.pop_state()

def exit():
    renderer.clear()

def pause():
    pass

def resume():
    pass

if __name__ == '__main__':
    core.start_state()