import os
from collections import deque, namedtuple

from kivy.core.audio import SoundLoader

from boxe_clock import utils

_here = os.path.dirname(__file__)

KIVY_STATIC_PATH = os.path.join(_here, "static")
KIVY_TEMPLATES_PATH = os.path.join(KIVY_STATIC_PATH, "templates")
KIVY_SOUNDS_PATH = os.path.join(KIVY_STATIC_PATH, "sounds")
KIVY_FONTS_PATH = os.path.join(KIVY_STATIC_PATH, "fonts")

TIMER_DEFAULTS = {
    "round_duration": 60 * 3,
    "warmup_duration": 10,
    "recovery_duration": 30,
}

Sound = namedtuple("Sound", ("name", "sound"))


def _load_current_sound(cls_method):
    def _inner(self, *args, **kwargs):
        try:
            return cls_method(self, *args, **kwargs)
        finally:
            name = self[0]
            path = os.path.join(KIVY_SOUNDS_PATH, utils.slugify(name) + ".wav")
            self.current = Sound(name, SoundLoader.load(path))

    return _inner


class SoundDeque(deque):
    """A collection that rotates and loads playable sounds.
    """

    @_load_current_sound
    def __init__(self, *args):
        super(SoundDeque, self).__init__(*args)

    @_load_current_sound
    def rotate(self, *args, **kwargs):
        super(SoundDeque, self).rotate(*args, **kwargs)


class TimerConfig(object):
    """A configuration namespace for Timers.
    """
    available_bells = ("Digital timer", "Ringside bell")

    def __init__(self, **kwargs):
        ns = {}
        ns.update(TIMER_DEFAULTS)
        ns.update(kwargs)
        self._namespace = ns
        self.bells = SoundDeque(self.available_bells)

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

    @staticmethod
    def fonts(name):
        return os.path.join(KIVY_FONTS_PATH, utils.slugify(name) + ".ttf")
