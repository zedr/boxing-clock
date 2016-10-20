from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, NumericProperty

from boxe_clock.constants import States, Colors
from boxe_clock.utils import format_time
from boxe_clock.platform.android import actions
from boxe_clock.config import TimerConfig


def _bell_enabled(method):
    def inner(self, widget, value):
        if value == 0:
            self.config.bell_sound.play()
        return method(self, widget, value)

    return inner


class TimerButton(Button):
    """The main clickable button.
    """
    markup = True
    default_round_duration = 60 * 3
    default_warmup_duration = 10
    default_cooldown_duration = 30
    clock_state = BooleanProperty()
    round_time = NumericProperty()
    warmup_time = NumericProperty()
    cooldown_time = NumericProperty()
    font_name = TimerConfig.fonts("Digital")
    font_size = 480

    def __init__(self, config=None):
        super(TimerButton, self).__init__()
        self.config = config or TimerConfig()
        self.reset()
        Clock.schedule_interval(lambda event: self.update(), 1)
        self.bind(
            on_touch_down=self._set_hold_event,
            on_touch_up=self._unset_hold_event,
        )

    def _set_hold_event(self, *args):
        self._hold_event = Clock.schedule_once(
            lambda event: self.reset(vibrate=True),
            1
        )

    def _unset_hold_event(self, *args):
        Clock.unschedule(self._hold_event)

    def _init_time(self, include_warmup=True):
        if include_warmup:
            self.warmup_time = self.default_warmup_duration
        self.cooldown_time = self.default_cooldown_duration
        self.round_time = self.default_round_duration

    def reset(self, vibrate=False):
        if vibrate:
            actions.vibrate()
        self._init_time()
        self.clock_state = States.PAUSED

    @_bell_enabled
    def on_round_time(self, widget, value):
        self.text = format_time(
            value,
            color=Colors.WHITE if value > 10 else Colors.RED
        )

    @_bell_enabled
    def on_warmup_time(self, widget, value):
        self.text = format_time(value, color=Colors.YELLOW)

    @_bell_enabled
    def on_cooldown_time(self, widget, value):
        self.text = format_time(
            value,
            color=Colors.GREEN if value > 10 else Colors.YELLOW
        )

    def on_clock_state(self, widget, value):
        if value:
            self.background_color = 0, 0, 0, 0
        else:
            self.background_color = 1, 1, 1, 1

    def on_press(self):
        self.toggle()

    def update(self):
        if self.clock_state == States.RUNNING:
            if self.warmup_time:
                self.warmup_time -= 1
            elif self.round_time:
                self.round_time -= 1
            elif self.cooldown_time:
                self.cooldown_time -= 1
            else:
                self._init_time(include_warmup=False)

    def toggle(self):
        self.clock_state ^= 1
