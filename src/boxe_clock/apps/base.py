from kivy.app import App

from boxe_clock.managers import AppRoot
from boxe_clock.config import KIVY_TEMPLATES_PATH


class BaseBoxingApp(App):
    """The base boxing clock app.
    """
    kv_directory = KIVY_TEMPLATES_PATH
    base_font_size = 480

    def build(self):
        return AppRoot(self.base_font_size)

    def on_start(self):
        pass

    def on_pause(self):
        return True
