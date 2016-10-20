from kivy.uix.carousel import Carousel

from boxe_clock.timer import TimerButton
from boxe_clock.layouts import ConfigLayout


class AppManager(Carousel):
    """The manager for the various screens used by the app.
    """
    direction = "right"

    def __init__(self, **kwargs):
        super(AppManager, self).__init__(**kwargs)
        self.timer_widget = TimerButton()
        self.config_widget = ConfigLayout()
        self.add_widget(self.timer_widget)
        self.add_widget(self.config_widget)
