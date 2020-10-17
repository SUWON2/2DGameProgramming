from pico2d import *

images = {}

def load(image_path):
    global images

    if image_path in images:
        return images[image_path]

    image = load_image(image_path)
    images[image_path] = image
    return image

def unload(image_path):
    global images

    if image_path in images:
        del images[image_path]

def clear():
    global images
    images.clear()