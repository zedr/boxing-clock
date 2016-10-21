import os

from kivy.core.audio import SoundLoader

from boxe_clock import utils

_here = os.path.dirname(__file__)

KIVY_STATIC_PATH = os.path.join(_here, "static")
KIVY_TEMPLATES_PATH = os.path.join(KIVY_STATIC_PATH, "templates")
KIVY_SOUNDS_PATH = os.path.join(KIVY_STATIC_PATH, "sounds")
KIVY_FONTS_PATH = os.path.join(KIVY_STATIC_PATH, "fonts")

TIMER_BELL_SOUNDS = ("Digital timer", "Ringside bell")

TIMER_DEFAULTS = {
    "round_duration": 60 * 3,
    "warmup_duration": 10,
    "cooldown_duration": 30,
}


class TimerConfig(object):
    """A configuration namespace for Timers.
    """
    available_bell_sound_names = TIMER_BELL_SOUNDS

    def __init__(self, **kwargs):
        ns = {}
        ns.update(TIMER_DEFAULTS)
        ns.update(kwargs)
        self._namespace = ns
        self.bell_sound_name = self.available_bell_sound_names[0]

    def __getattr__(self, name):
        try:
            return self._namespace[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, key, value):
        """Only set attributes in the namespace if the key already exists.
        """
        if key != "_namespace" and key in self._namespace:
            self._namespace[key] = value
        else:
            super(TimerConfig, self).__setattr__(key, value)

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
