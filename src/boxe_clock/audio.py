import os
import functools
from collections import deque, namedtuple

from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from boxe_clock import utils
from boxe_clock.constants import KIVY_SOUNDS_PATH

Sound = namedtuple("Sound", ("name", "sound"))


def bell_on_zero(method):
    @functools.wraps(method)
    def inner(self, widget, value):
        if value == 0:
            self.config.bells.current.sound.play()
        return method(self, widget, value)

    return inner


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
