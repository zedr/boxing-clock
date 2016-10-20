from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

from boxe_clock import config
from boxe_clock.timer import TimerButton


class TimerScreen(Screen):
    def __init__(self, **kwargs):
        super(TimerScreen, self).__init__(**kwargs)
        self.add_widget(TimerButton())


class ConfigMenu(GridLayout):
    font_name = config.fonts("digi.ttf")
    bell_sound = config.audio("bell2.wav")


class TimerScreenManager(Carousel):
    """An object that manages the various timer screens.
    """
    direction = "right"

    def __init__(self, **kwargs):
        super(TimerScreenManager, self).__init__(**kwargs)
        self.timer_screen = TimerScreen()
        self.config_menu = ConfigMenu()
        self.add_widget(self.timer_screen)
        self.add_widget(self.config_menu)
