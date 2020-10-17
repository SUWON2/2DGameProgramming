from pico2d import *

import core
import title_state

const = core.constants
renderer = core.renderer
sprite = core.sprite

logo = None
elapsed_time = 0

def init():
    global logo

    logo = sprite.Sprite('res/kpu_logo.png')
    logo.x = const.SCREEN_WIDTH / 2
    logo.y = const.SCREEN_HEIGHT / 2
    renderer.Add(logo)

def update():
    global elapsed_time

    elapsed_time += core.delta_time
    if elapsed_time >= 1.0:
        core.change_state(title_state)
        return
        
def exit():
    renderer.clear()

def pause():
    pass

def resume():
    pass

if __name__ == '__main__':
    core.start_state()