import os
from collections import deque, namedtuple

from kivy.core.audio import SoundLoader

from boxe_clock import utils
from boxe_clock import defaults

_here = os.path.dirname(__file__)

KIVY_STATIC_PATH = os.path.join(_here, "static")
KIVY_TEMPLATES_PATH = os.path.join(KIVY_STATIC_PATH, "templates")
KIVY_SOUNDS_PATH = os.path.join(KIVY_STATIC_PATH, "sounds")
KIVY_FONTS_PATH = os.path.join(KIVY_STATIC_PATH, "fonts")

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
    """A singleton configuration namespace for the Timer.
    """
    bells = SoundDeque(("Digital timer", "Ringside bell"))
    round_duration = defaults.ROUND_DURATION
    warmup_duration = defaults.WARMUP_DURATION
    recovery_duration = defaults.RECOVERY_DURATION
    rounds_max = defaults.ROUNDS_MAX

    @staticmethod
    def fonts(name):
        return os.path.join(KIVY_FONTS_PATH, utils.slugify(name) + ".ttf")
