from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.uix.button import Button

from boxe_clock.constants import States, Colors
from boxe_clock.utils import format_time
from boxe_clock.decorators import bell_enabled


class TimerButton(Button):
    """The main clickable button.
    """
    markup = True
    default_round_duration = 60 * 3
    default_warmup_duration = 10
    default_cooldown_duration = 30
    formatted_time = StringProperty()
    clock_state = BooleanProperty()
    round_time = NumericProperty()
    warmup_time = NumericProperty()
    cooldown_time = NumericProperty()
    bell_sound_name = "boxe_clock/static/sounds/bell.wav"
    font_name = "boxe_clock/static/fonts/digi.ttf"

    def __init__(self):
        super(TimerButton, self).__init__()
        self._init_time()
        self.bell_sound = SoundLoader.load(self.bell_sound_name)
        self.clock_state = States.PAUSED
        Clock.schedule_interval(lambda event: self.update(), 1)

    def _init_time(self, include_warmup=True):
        if include_warmup:
            self.warmup_time = self.default_warmup_duration
        self.cooldown_time = self.default_cooldown_duration
        self.round_time = self.default_round_duration

    @bell_enabled
    def on_round_time(self, widget, value):
        self.formatted_time = format_time(
            value,
            color=Colors.WHITE if value > 10 else Colors.RED
        )

    @bell_enabled
    def on_warmup_time(self, widget, value):
        self.formatted_time = format_time(value, color=Colors.YELLOW)

    @bell_enabled
    def on_cooldown_time(self, widget, value):
        self.formatted_time = format_time(
            value,
            color=Colors.GREEN if value > 10 else Colors.YELLOW
        )

    def on_clock_state(self, widget, value):
        if value:
            self.background_color = 0, 0, 0, 0
        else:
            self.background_color = 1, 1, 1, 1

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
