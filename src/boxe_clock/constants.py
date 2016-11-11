import os

_here = os.path.dirname(__file__)

KIVY_STATIC_PATH = os.path.join(_here, "static")
KIVY_TEMPLATES_PATH = os.path.join(KIVY_STATIC_PATH, "templates")
KIVY_SOUNDS_PATH = os.path.join(KIVY_STATIC_PATH, "sounds")
KIVY_FONTS_PATH = os.path.join(KIVY_STATIC_PATH, "fonts")


class States(object):
    PAUSED = 0
    RUNNING = 1


class Colors(object):
    WHITE = "fff"
    RED = "f33"
    YELLOW = "ff3"
    GREEN = "3f3"
    CYAN = "ccf"
