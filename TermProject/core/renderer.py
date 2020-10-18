import math
import core.cache_image as cimage
import core.sprite as sprite

sprites = []

def draw():
    global sprites

    for spr in sprites:
        assert spr.image, "이미지가 등록되어 있지 않습니다."
        
        spr.image.opacify(spr.alpha)
        spr.image.rotate_draw(math.radians(spr.angle), spr.x, spr.y, spr.image.w * spr.scaleX, spr.image.h * spr.scaleY)

def Add(spr):
    global sprites

    assert not spr in sprites
    sprites.append(spr)

def remove(spr):
    global sprites

    assert spr in sprites, "등록되지 않은 이미지를 제거할 수 없습니다."
    sprites.remove(spr)

def clear():
    global sprties;

    cimage.clear()
    sprites.clear()