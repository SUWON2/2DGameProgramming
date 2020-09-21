from pico2d import *

open_canvas()

ch = load_image('../res/character.png')

for y in range(100, 500 + 1, 100):
    for x in range(100, 700 + 1, 100):
        ch.draw_now(x, y)

delay(2) # in seconds

close_canvas()