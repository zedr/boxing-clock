import os

from kivy.core.audio import SoundLoader

from boxe_clock import utils

_here = os.path.dirname(__file__)

KIVY_STATIC_PATH = os.path.join(_here, "static")
KIVY_TEMPLATES_PATH = os.path.join(KIVY_STATIC_PATH, "templates")
KIVY_SOUNDS_PATH = os.path.join(KIVY_STATIC_PATH, "sounds")
KIVY_FONTS_PATH = os.path.join(KIVY_STATIC_PATH, "fonts")

BELL_SOUNDS = ("Digital timer", "Ringside bell")


class TimerConfig(object):
    """A configuration namespace for Timers.
    """
    available_bell_sound_names = BELL_SOUNDS

    def __init__(self):
        self.bell_sound = self.available_bell_sound_names[0]

    @property
    def bell_sound(self):
        return self._bell_sound

    @bell_sound.setter
    def bell_sound(self, name):
        path = os.path.join(
            KIVY_SOUNDS_PATH,
            utils.slugify(name) + ".wav"
        )
        self._bell_sound = SoundLoader.load(path)

    @staticmethod
    def fonts(name):
        return os.path.join(KIVY_FONTS_PATH, utils.slugify(name) + ".ttf")
