from pico2d import *

import core.constants as const

LBUTTON = 0
MBUTTON = 1
RBUTTON = 2
BUTTON_COUNT = 3

pressing_keys = {}
changed_keys = {}

mouse_pos = (0, 0)
pressing_buttons = [False for i in range(BUTTON_COUNT)]
changed_buttons = [False for i in range(BUTTON_COUNT)]

def update():
    global pressing_keys
    global changed_keys
    global mouse_pos
    global pressing_buttons
    global changed_buttons

    changed_keys.clear()
    changed_buttons = [False for i in range(BUTTON_COUNT)]

    events = get_events()
    for e in events:
        if e.type == SDL_KEYDOWN:
            changed_keys[e.key] = True
            pressing_keys[e.key] = True
        elif e.type == SDL_KEYUP:
            changed_keys[e.key] = True
            pressing_keys[e.key] = False
        elif e.type == SDL_MOUSEMOTION:
            mouse_pos = (e.x - const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2 - e.y)
        elif e.type == SDL_MOUSEBUTTONDOWN:
            index = e.button - 1
            changed_buttons[index] = True
            pressing_buttons[index] = True
        elif e.type == SDL_MOUSEBUTTONUP:
            index = e.button - 1
            changed_buttons[index] = True;
            pressing_buttons[index] = False
        elif e.type == SDL_QUIT:
            return False

    return True

def get_key(key):
    global pressing_keys
    return key in pressing_keys and pressing_keys[key]

def get_key_down(key):
    global changed_keys
    return key in changed_keys and changed_keys[key] and get_key(key)

def get_key_up(key):
    global changed_keys
    return key in changed_keys and changed_keys[key] and get_key(key) == False

def get_mouse_pos():
    return mouse_pos

def get_mouse_button(button):
    assert LBUTTON <= button and button < BUTTON_COUNT, '지원하지 않는 버튼입니다.'

    global pressing_buttons
    return pressing_buttons[button]

def get_mouse_button_down(button):
    assert LBUTTON <= button and button < BUTTON_COUNT, '지원하지 않는 버튼입니다.'

    global changed_buttons
    return changed_buttons[button] and pressing_buttons[button]

def get_mouse_button_up(button):
    assert LBUTTON <= button and button < BUTTON_COUNT, '지원하지 않는 버튼입니다.'

    global changed_buttons
    return changed_buttons[button] and pressing_buttons[button] == False