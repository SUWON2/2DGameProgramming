import math
import core.cache_image
import core.sprite
import core.cache_font
import core.text
import core.camera

sprites = []
texts = []

def update():
    global sprites
    global texts

    core.camera.update()

    for spr in sprites:
        if spr.active == False:
            continue

        assert spr.image, '이미지가 등록되어 있지 않습니다.'
        
        to_x = spr.x + spr.image.w * spr.scaleX * (0.5 - spr.origin_x)
        to_y = spr.y + spr.image.h * spr.scaleY * (0.5 - spr.origin_y)
        if not spr.camera_ignorer:
            to_x -= core.camera.x
            to_y -= core.camera.y

        spr.image.opacify(spr.alpha)
        spr.image.rotate_draw(math.radians(spr.angle), to_x, to_y, spr.image.w * spr.scaleX, spr.image.h * spr.scaleY)

    for text in texts:
        if text.active == False:
            continue

        assert text.ttf, '폰트가 등록되어 있지 않습니다.'
        text.ttf.draw(text.x, text.y, text.text, (text.color_r, text.color_g, text.color_b))

def Add(obj):
    global sprites
    global texts

    obj_type = type(obj)
    if obj_type == core.sprite.Sprite:
        assert not obj in sprites, '이미 등록된 스프라이트입니다.'
        sprites.append(obj)
    elif obj_type == core.text.Text:
        assert not obj in texts, '이미 등록된 폰트입니다.'
        texts.append(obj)
    else:
        assert False, 'Sprite 혹은 Font 타입만 지원합니다.'

def remove(obj):
    global sprites
    global texts

    obj_type = type(obj)
    if obj_type == core.sprite.Sprite:
        assert obj in sprites, '등록되지 않은 스프라이트를 제거할 수 없습니다.'
        sprites.remove(obj)
    elif obj_type == core.text.Text:
        assert obj in texts, '등록되지 않은 폰트를 제거할 수 없습니다.'
        texts.remove(obj)
    else:
        assert False, 'Sprite 혹은 Font 타입만 지원합니다.'

def clear():
    global sprites;
    global texts

    core.cache_image.clear()
    sprites.clear()

    core.cache_font.clear()
    texts.clear()

    core.camera.clear()