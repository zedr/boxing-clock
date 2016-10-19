from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager

from boxe_clock import config
from boxe_clock.timer import TimerButton


class TimerScreen(Screen):
    def __init__(self, **kwargs):
        super(TimerScreen, self).__init__(**kwargs)
        self.add_widget(TimerButton())


class ConfigMenu(GridLayout):
    font_name = config.fonts("digi.ttf")
    bell_sound = config.audio("bell2.wav")


class ConfigScreen(Screen):
    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(**kwargs)
        self.add_widget(ConfigMenu())


class TimerScreenManager(ScreenManager):
    """An object that manages the various timer screens.
    """

    def __init__(self, **kwargs):
        super(TimerScreenManager, self).__init__(**kwargs)
        self.timer_screen = TimerScreen()
        self.config_screen = ConfigScreen()
        self.switch_to(self.timer_screen)
