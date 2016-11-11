import os

from kivy.storage.jsonstore import JsonStore

from boxe_clock import utils
from boxe_clock import defaults
from boxe_clock.constants import KIVY_FONTS_PATH
from boxe_clock.audio import SoundDeque



class TimerConfig(object):
    """A singleton configuration namespace for the Timer.
    """
    _storage_name = "timer"
    bells = SoundDeque(("Digital timer", "Ringside bell", "Silence"))

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
