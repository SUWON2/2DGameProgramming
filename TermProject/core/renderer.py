import math
import core.cache_image
import core.sprite
import core.camera

sprites = []

def draw():
    global sprites

    offsetX = -core.camera.x + core.constants.SCREEN_WIDTH / 2
    offsetY = -core.camera.y + core.constants.SCREEN_HEIGHT / 2

    for spr in sprites:
        assert spr.image, '이미지가 등록되어 있지 않습니다.'
        
        to_x = spr.x
        to_y = spr.y
        if not spr.camera_ignorer:
            to_x += offsetX
            to_y += offsetY

        spr.image.opacify(spr.alpha)
        spr.image.rotate_draw(math.radians(spr.angle), to_x, to_y, spr.image.w * spr.scaleX, spr.image.h * spr.scaleY)

def Add(spr):
    global sprites

    assert not spr in sprites, '이미 등록된 스프라이트입니다.'
    sprites.append(spr)

def remove(spr):
    global sprites

    assert spr in sprites, '등록되지 않은 이미지를 제거할 수 없습니다.'
    sprites.remove(spr)

def clear():
    global sprties;

    core.cache_image.clear()
    sprites.clear()