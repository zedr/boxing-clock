import logging
from collections import namedtuple

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.properties import StringProperty

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

states = namedtuple("States", ("PAUSED", "RUNNING"))(*range(2))


class Time(int):
    @property
    def minutes(self):
        return self // 60

    @property
    def seconds(self):
        return self % 60

    def __str__(self):
        return "{0}:{1:02d}".format(self.minutes, self.seconds)

    def __isub__(self, other):
        return Time(self - other)

    def __iadd__(self, other):
        return Time(self + other)


class TimerButton(Button):
    """The main clickable button.
    """
    default_round_duration = 180
    formatted_time = StringProperty()

    def __init__(self):
        super(TimerButton, self).__init__()
        self.time = Time(self.default_round_duration)
        self.clock_state = states.PAUSED
        self._text_state = 0
        Clock.schedule_interval(self.update, 1)

    def _update_formatted_time(self):
        self.formatted_time = str(self._time)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        self._update_formatted_time()

    def update(self, *args):
        if self.clock_state == states.RUNNING:
            self.time -= 1


class BoxingApp(App):
    def build(self):
        return TimerButton()


def main():
    BoxingApp().run()


if __name__ == "__main__":
    main()
