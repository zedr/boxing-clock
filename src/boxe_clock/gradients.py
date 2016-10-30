# Taken from https://groups.google.com/forum/#!topic/kivy-users/Go7HINbBtI0
from kivy.graphics.texture import Texture


class Gradient(object):
    @staticmethod
    def horizontal(rgba_left, rgba_right):
        # noinspection PyArgumentList
        texture = Texture.create(size=(2, 1), colorfmt="rgba")
        pixels = rgba_left + rgba_right
        pixels = [chr(int(v * 255)) for v in pixels]
        buf = ''.join(pixels)
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

    @staticmethod
    def vertical(rgba_top, rgba_bottom):
        # noinspection PyArgumentList
        texture = Texture.create(size=(1, 2), colorfmt="rgba")
        pixels = rgba_bottom + rgba_top
        pixels = [chr(int(v * 255)) for v in pixels]
        buf = ''.join(pixels)
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture
