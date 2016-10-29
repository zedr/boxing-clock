import os
from collections import deque, namedtuple

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.storage.jsonstore import JsonStore

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
            path = os.path.join(KIVY_SOUNDS_PATH, utils.slugify(name) + ".mp3")
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

    def select(self, name):
        if name in self:
            while self[0] != name:
                self.rotate()

    def play_current(self, times=1, timeout=0.5):
        """Play the currently loaded sound a certain amount of times.
        """
        if self.current.sound.state != "play":
            self.current.sound.play()
            times -= 1
        if times > 0:
            Clock.schedule_once(
                lambda ev: self.play_current(times, timeout),
                timeout=timeout
            )


class TimerConfig(object):
    """A singleton configuration namespace for the Timer.
    """
    _storage_name = "timer"
    bells = SoundDeque(("Digital timer", "Ringside bell"))

    def __init__(self):
        storage = JsonStore(defaults.DATABASE_NAME)
        if storage.exists(self._storage_name):
            bell_name = storage[self._storage_name].get("bell_name")
            self.bells.select(bell_name)
        else:
            storage[self._storage_name] = {
                "round_duration": defaults.ROUND_DURATION,
                "warmup_duration": defaults.WARMUP_DURATION,
                "recovery_duration": defaults.RECOVERY_DURATION,
                "rounds_max": defaults.ROUNDS_MAX,
                "bell_name": self.bells.current.name
            }
        self._storage = storage

    def _get_key(self, key):
        return self._storage[self._storage_name].get(key)

    def _set_key(self, key, value):
        """Update the storage every time a key is set.
        """
        storage_name = self._storage_name
        ns = self._storage[storage_name]
        ns[key] = value
        self._storage.put(storage_name, **ns)

    def _has_key(self, key):
        return key in self._storage[self._storage_name]

    def __getattr__(self, key):
        try:
            return self._get_key(key)
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key == "_storage":
            super(TimerConfig, self).__setattr__(key, value)
        else:
            if self._has_key(key):
                self._set_key(key, value)
            else:
                raise AttributeError("Cannot set attribute: {0}".format(key))

    @staticmethod
    def fonts(name):
        return os.path.join(KIVY_FONTS_PATH, utils.slugify(name) + ".ttf")
