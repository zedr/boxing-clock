from kivy.uix.carousel import Carousel

from boxe_clock.timer import TimerButton
from boxe_clock.menus import ConfigMenu
from boxe_clock.config import TimerConfig


class AppManager(Carousel):
    """The manager for the various screens used by the app.
    """
    direction = "right"

    def __init__(self, **kwargs):
        super(AppManager, self).__init__(**kwargs)
        config = TimerConfig()
        self.config_widget = ConfigMenu(config)
        self.timer_widget = TimerButton(config)
        self.add_widget(self.timer_widget)
        self.add_widget(self.config_widget)
