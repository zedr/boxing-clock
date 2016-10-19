from kivy.app import App

from boxe_clock.screens import TimerScreenManager
from boxe_clock.config import KIVY_TEMPLATES_PATH


class BaseBoxingApp(App):
    kv_directory = KIVY_TEMPLATES_PATH

    def build(self):
        return TimerScreenManager()

    def on_start(self):
        pass

    def on_pause(self):
        return True
