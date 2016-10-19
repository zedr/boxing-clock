import os

_here = os.path.dirname(__file__)

KIVY_STATIC_PATH = os.path.join(_here, "static")
KIVY_TEMPLATES_PATH = os.path.join(KIVY_STATIC_PATH, "templates")
KIVY_SOUNDS_PATH = os.path.join(KIVY_STATIC_PATH, "sounds")
KIVY_FONTS_PATH = os.path.join(KIVY_STATIC_PATH, "fonts")


def audio(filename):
    return os.path.join(KIVY_SOUNDS_PATH, filename)


def fonts(filename):
    return os.path.join(KIVY_FONTS_PATH, filename)
