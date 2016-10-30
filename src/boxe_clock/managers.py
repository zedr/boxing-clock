from kivy.uix.carousel import Carousel

from boxe_clock.config import TimerConfig


class AppRoot(Carousel):
    """The App root widget.

    This is a Carousel that alternates between the timer and the configuration
    screen.
    """
    direction = "right"

    def __init__(self, **kwargs):
        self.timer_config = TimerConfig()
        super(AppRoot, self).__init__(**kwargs)
