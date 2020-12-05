import random
import core

x = 0.0
y = 0.0
shake_amount = 0.0
shake_duration = 0.0

def update():
    global x, y
    global shake_duration
    global shake_amount

    if shake_duration >= 0.0:
        x += random.uniform(-shake_amount, shake_amount)
        y += random.uniform(-shake_amount, shake_amount)

        shake_duration -= core.delta_time
        if shake_duration < 0.0:
            shake_amount = 0.0
            shake_duration = 0.0

def clear():
    global x, y
    
    x = 0.0
    y = 0.0

def shake(amount, duration):
    global shake_duration
    global shake_amount

    if shake_amount < amount:
        shake_amount = amount

    if shake_duration < duration:
        shake_duration = duration