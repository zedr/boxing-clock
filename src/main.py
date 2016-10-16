import logging
from collections import namedtuple

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.properties import StringProperty, BooleanProperty, NumericProperty

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

states = namedtuple("States", ("PAUSED", "RUNNING"))(*range(2))


def format_time(seconds):
    return "{0}:{1:02d}".format(seconds // 60, seconds % 60)


class TimerButton(Button):
    """The main clickable button.
    """
    default_round_duration = 180
    default_warmup_duration = 10
    formatted_time = StringProperty()
    clock_state = BooleanProperty()
    round_time = NumericProperty()
    warmup_time = NumericProperty()

    def __init__(self):
        super(TimerButton, self).__init__()
        self._init_time()
        self.clock_state = states.PAUSED
        Clock.schedule_interval(lambda event: self.update(), 1)

    def _init_time(self):
        self.round_time = self.default_round_duration
        self.warmup_time = self.default_warmup_duration

    def on_round_time(self, widget, value):
        self.formatted_time = format_time(value)

    def on_warmup_time(self, widget, value):
        self.formatted_time = format_time(value)

    def on_clock_state(self, widget, value):
        if value:
            self.background_color = 0, 0, 0, 0
        else:
            self.background_color = 1, 1, 1, 1

    def update(self):
        if self.clock_state == states.RUNNING:
            if self.warmup_time:
                self.warmup_time -= 1
            elif self.round_time:
                self.round_time -= 1
            else:
                self._init_time()


    def toggle(self):
        self.clock_state ^= 1


class BoxingApp(App):
    def build(self):
        return TimerButton()


def main():
    BoxingApp().run()


if __name__ == "__main__":
    main()
