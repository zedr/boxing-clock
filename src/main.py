import logging
from collections import namedtuple

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.properties import StringProperty, BooleanProperty

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
    default_round_duration = 15
    formatted_time = StringProperty()
    clock_state = BooleanProperty()

    def __init__(self):
        super(TimerButton, self).__init__()
        self._init_round_time()
        self.clock_state = states.PAUSED
        Clock.schedule_interval(lambda event: self.update(), 1)

    def _update_formatted_time(self):
        self.formatted_time = str(self._round_time)

    @property
    def round_time(self):
        return self._round_time

    @round_time.setter
    def round_time(self, value):
        self._round_time = value
        self._update_formatted_time()

    def on_clock_state(self, widget, value):
        if value:
            self.background_color = 0, 0, 0, 0
        else:
            self.background_color = 1, 1, 1, 1

    def _init_round_time(self):
        self.round_time = Time(self.default_round_duration)

    def update(self):
        if self.clock_state == states.RUNNING:
            if self.round_time > 0:
                self.round_time -= 1
            else:
                self._init_round_time()

    def toggle(self):
        self.clock_state ^= 1


class BoxingApp(App):
    def build(self):
        return TimerButton()


def main():
    BoxingApp().run()


if __name__ == "__main__":
    main()
