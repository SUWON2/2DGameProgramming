from pico2d import *

import core
import game_state

eh = core.events_handler

def init():
    pass

def update():
    if eh.get_key_down(SDLK_SPACE):
        core.push_state(game_state)
        return
    elif eh.get_key_down(SDLK_ESCAPE):
        core.pop_state()
        return

def exit():
    pass

def pause():
    pass

def resume():
    pass

if __name__ == '__main__':
    core.start_state()