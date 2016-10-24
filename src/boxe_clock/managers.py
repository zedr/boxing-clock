from kivy.uix.carousel import Carousel

from boxe_clock.menus import ConfigMenu
from boxe_clock.config import TimerConfig


class AppRoot(Carousel):
    def __init__(self, base_font_size, **kwargs):
        self.base_font_size = base_font_size
        self.timer_config = TimerConfig()
        super(AppRoot, self).__init__(**kwargs)


class AppManager(Carousel):
    """The manager for the various screens used by the app.
    """
    direction = "right"

    def __init__(self, **kwargs):
        super(AppManager, self).__init__(**kwargs)
        config = TimerConfig()
        self.config_widget = ConfigMenu(config)
        self.add_widget(self.timer_widget)
        self.add_widget(self.config_widget)
