import time
from pico2d import *

import core.constants as const
import core.events_handler as eh
import core.renderer
import core.sprite

running = True
delta_time = 0
states = None

def init(state):
    global states

    open_canvas(const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
    SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, b"1")
    hide_lattice()
    hide_cursor()
    
    states = [state]
    state.init()

def run():
    global states
    global delta_time

    while running:
        start_time = time.time()

        if eh.update() == False:
            break

        states[-1].update()

        clear_canvas()
        core.renderer.draw()
        update_canvas()

        delay_time = 1.0 / const.FPS - (time.time() - start_time)
        if delay_time > 0.0:
            delay(delay_time)

        delta_time = time.time() - start_time

    while states:
        states[-1].exit()
        states.pop()

    core.renderer.clear()

    close_canvas()

def quit():
    global running
    running = False

def change_state(state):
    global states

    if states:
        states[-1].exit()
        states.pop()

    states.append(state)
    state.init()

def push_state(state):
    global states

    if states:
        states[-1].pause()

    states.append(state)
    state.init()

def pop_state():
    global states

    if len(states) > 1:
        states[-1].exit()
        states.pop()

        states[-1].resume()
    else:
        quit()