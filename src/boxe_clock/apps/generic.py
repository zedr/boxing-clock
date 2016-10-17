from kivy.app import App

from boxe_clock.timer import TimerButton
from boxe_clock.config import KIVY_TEMPLATES_PATH


class BoxingApp(App):
    kv_directory = KIVY_TEMPLATES_PATH

    def build(self):
        return TimerButton()

    def on_start(self):
        pass

    def on_pause(self):
        return True
