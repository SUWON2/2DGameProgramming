from pico2d import *

import core
import title_state

const = core.constants
elapsed_time = 0
logo_image = None

def init():
    global logo_image
    logo_image = load_image('res/kpu_logo.png')

def update():
    global elapsed_time
    global logo_image

    elapsed_time += core.delta_time
    if elapsed_time >= 1.0:
        core.change_state(title_state)

    logo_image.draw(const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2)

def exit():
    pass

def pause():
    pass

def resume():
    pass

if __name__ == '__main__':
    core.start_state()