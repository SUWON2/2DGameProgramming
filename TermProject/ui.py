import core

class UI:
    def __init__(self, idle_image_path, contact_image_path = None):
        self.spr = core.Sprite(idle_image_path)
        core.renderer.Add(self.spr)

        self.idle_image_path = idle_image_path
        self.contact_image_path = contact_image_path

    def __del__(self):
        core.renderer.remove(self.spr)

    def update(self):
        if not self.contact_image_path is None:
            if self.is_mouse_contacted():
                self.spr.set_image(self.contact_image_path)
            else:
                self.spr.set_image(self.idle_image_path)

    def move_to(self, x, y, speed):
        self.spr.x += (x - self.spr.x) * speed * core.delta_time
        self.spr.y += (y - self.spr.y) * speed * core.delta_time

    def is_mouse_contacted(self):
        mouse_x, mouse_y = core.eh.mouse_pos[0], core.eh.mouse_pos[1]

        x = self.spr.x + self.spr.image.w * (0.5 - self.spr.origin_x)
        y = self.spr.y + self.spr.image.h * (0.5 - self.spr.origin_y)
        half_size_x = self.spr.image.w * self.spr.scaleX * 0.5
        half_size_y = self.spr.image.h * self.spr.scaleY * 0.5

        return x - half_size_x <= mouse_x and mouse_x <= x + half_size_x  and y - half_size_y <= mouse_y and mouse_y <= y + half_size_y

    def is_pressed(self):
        return self.is_mouse_contacted() and core.eh.get_mouse_button_down(core.eh.LBUTTON)