from kivy import properties
from kivy.clock import Clock
from kivy.uix.button import Button

from boxe_clock import utils
from boxe_clock import audio
from boxe_clock.constants import Colors, States
from boxe_clock.mixins import LedMixin
from boxe_clock.config import TimerConfig
from boxe_clock.platform.android import actions


class LedButton(LedMixin, Button):
    """A LED button.
    """
    background_color = (0, 0, 0, 0)


class TimerButton(LedButton):
    """The button that activates, pauses, and resets the timer clock.
    """
    clock_state = properties.BooleanProperty()
    clock_state_verbose = properties.StringProperty()
    round_time = properties.NumericProperty()
    warmup_time = properties.NumericProperty()
    recovery_time = properties.NumericProperty()
    round_number = properties.NumericProperty()
    round_verbose = properties.StringProperty()
    config = TimerConfig

    def __init__(self, **kwargs):
        super(TimerButton, self).__init__(**kwargs)
        self.clock_state = States.PAUSED
        self._init_time()
        self.bind(
            on_press=self._set_hold_event,
            on_release=self._unset_hold_event,
        )

    def _set_hold_event(self, *args):
        self._hold_event = Clock.schedule_once(
            lambda event: self.reset(vibrate=True),
            0.5
        )

    def _unset_hold_event(self, *args):
        Clock.unschedule(self._hold_event)

    def _init_time(self, complete=True):
        # Warmup isn't typically used between rounds.
        if complete:
            self.warmup_time = TimerConfig.warmup_duration
            self.round_number = 1
            self.on_round_number(None, 1)
        self.recovery_time = TimerConfig.recovery_duration
        # Round time comes last so its duration is displayed on the clock.
        self.round_time = TimerConfig.round_duration

    def _start_ticking(self):
        self._update_ticker = Clock.schedule_interval(
            lambda ev: self.update(), 1
        )

    def _stop_ticking(self):
        try:
            Clock.unschedule(self._update_ticker)
        except AttributeError:
            pass

    def reset(self, vibrate=False):
        if vibrate:
            actions.vibrate()
        self.clock_state = States.PAUSED
        self._stop_ticking()
        self._init_time(complete=True)

    def toggle(self):
        """Toggle the PAUSED/ACTIVE states.
        """
        self.clock_state ^= 1
        if self.clock_state:
            self._start_ticking()
        else:
            self._stop_ticking()

    def update(self):
        if self.warmup_time:
            self.warmup_time -= 1
        elif self.round_time:
            self.round_time -= 1
        elif self.recovery_time:
            self.recovery_time -= 1
        else:
            self.round_number += 1
            if self.round_number > self.config.rounds_max:
                self.reset()
            else:
                self._init_time(complete=False)

    def on_clock_state(self, widget, state):
        if state:
            actions.dim()
        self.clock_state_verbose = "" if state else "Paused"

    @audio.bell_on_zero
    def on_round_time(self, widget, time):
        self.text = utils.format_time(
            time,
            color=Colors.WHITE if time > 10 else Colors.RED
        )

    @audio.bell_on_zero
    def on_warmup_time(self, widget, time):
        self.text = utils.format_time(time, color=Colors.YELLOW)

    @audio.bell_on_zero
    def on_recovery_time(self, widget, time):
        self.text = utils.format_time(
            time,
            color=Colors.GREEN if time > 10 else Colors.YELLOW
        )

    def on_round_number(self, widget, round_number):
        self.round_verbose = "{0}/{1}".format(
            round_number, self.config.rounds_max
        )
