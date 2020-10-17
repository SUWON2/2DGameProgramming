import time
from pico2d import *

import core.constants as const
import core.events_handler as eh

running = True
states = None
delta_time = 0

def run(state):
    global states
    global delta_time

    states = [state]

    open_canvas(const.SCREEN_WIDTH, const.SCREEN_HEIGHT)

    state.init()

    while running:
        start_time = time.time()

        if eh.update() == False:
            break

        clear_canvas()
        states[-1].update()
        update_canvas()

        delay_time = 1.0 / const.FPS - (time.time() - start_time)
        if delay_time > 0.0:
            delay(delay_time)

        delta_time = time.time() - start_time

    while states:
        states[-1].exit()
        states.pop()

    close_canvas()

def quit():
    global running
    running = False

def start_state():
    import sys
    run(sys.modules['__main__'])

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