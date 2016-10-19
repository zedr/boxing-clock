from kivy.uix.screenmanager import Screen, ScreenManager

from boxe_clock.timer import TimerButton


class TimerScreen(Screen):
    def __init__(self, **kwargs):
        super(TimerScreen, self).__init__(**kwargs)
        self.add_widget(TimerButton())


class TimerScreenManager(ScreenManager):
    """An object that manages the various timer screens.
    """

    def __init__(self, **kwargs):
        super(TimerScreenManager, self).__init__(**kwargs)
        self.timer_screen = TimerScreen()
        self.switch_to(self.timer_screen)
