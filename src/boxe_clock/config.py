import os

from kivy.core.audio import SoundLoader

from boxe_clock import utils

_here = os.path.dirname(__file__)

KIVY_STATIC_PATH = os.path.join(_here, "static")
KIVY_TEMPLATES_PATH = os.path.join(KIVY_STATIC_PATH, "templates")
KIVY_SOUNDS_PATH = os.path.join(KIVY_STATIC_PATH, "sounds")
KIVY_FONTS_PATH = os.path.join(KIVY_STATIC_PATH, "fonts")

BELL_SOUNDS = ("Digital timer", "Ringside bell")

DEFAULTS = {
    "round_duration": 60 * 3,
    "warmup_duration": 10,
    "cooldown_duration": 30,
}


class TimerConfig(object):
    """A configuration namespace for Timers.
    """
    available_bell_sound_names = BELL_SOUNDS

    def __init__(self, **kwargs):
        self.bell_sound_name = self.available_bell_sound_names[0]
        ns = {}
        ns.update(DEFAULTS)
        ns.update(kwargs)
        self._namespace = ns

    def __getattr__(self, name):
        try:
            return self._namespace[name]
        except KeyError:
            raise AttributeError(name)

    @property
    def bell_sound_name(self):
        return self._bell_sound_name

    @bell_sound_name.setter
    def bell_sound_name(self, name):
        path = os.path.join(
            KIVY_SOUNDS_PATH,
            utils.slugify(name) + ".wav"
        )
        self.bell_sound = SoundLoader.load(path)
        self._bell_sound_name = name

    @staticmethod
    def fonts(name):
        return os.path.join(KIVY_FONTS_PATH, utils.slugify(name) + ".ttf")
