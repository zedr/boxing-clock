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

    def __init__(self, **kwargs):
        super(TimerButton, self).__init__(**kwargs)
        self.clock_state = States.PAUSED
        self.config = TimerConfig()
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
            self.warmup_time = self.config.warmup_duration
            self.round_number = 1
            self.on_round_number(None, 1)
        self.recovery_time = self.config.recovery_duration
        # Round time comes last so its duration is displayed on the clock.
        self.round_time = self.config.round_duration

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

    @property
    def is_at_final_round(self):
        """Is the timer at its final round?
        """
        return self.round_number >= self.config.rounds_max

    def update(self):
        """Run an update cycle.
        """
        if self.warmup_time:
            self.warmup_time -= 1
        elif self.round_time:
            self.round_time -= 1
            if not self.round_time and self.is_at_final_round:
                # End of final round: play the bell two more times.
                self.config.bells.play_current(times=2)
        elif self.recovery_time:
            self.recovery_time -= 1
        else:
            if self.is_at_final_round:
                # End of training routine.
                self.reset()
            else:
                self.round_number += 1
                self._init_time(complete=False)

    def _start_messaging(self):
        def _callback(ev):
            if self.clock_state_verbose == "Paused":
                self.clock_state_verbose = "Hold to reset"
            else:
                self.clock_state_verbose = "Paused"

        _callback(None)
        self._message_ticker = Clock.schedule_interval(_callback, 1)

    def _stop_messaging(self):
        Clock.unschedule(self._message_ticker)

    def on_clock_state(self, widget, state):
        if state:
            self._stop_messaging()
            actions.dim()
            self.clock_state_verbose = ""
        else:
            self._start_messaging()

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
