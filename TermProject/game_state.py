from pico2d import *

import core

eh = core.events_handler

def init():
    pass

def update():
    if eh.get_key_down(SDLK_ESCAPE):
        core.pop_state()

def exit():
    pass

def pause():
    pass

def resume():
    pass

if __name__ == '__main__':
    core.start_state()