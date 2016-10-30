# noinspection PyUnresolvedReferences
from android.runnable import run_on_ui_thread

from boxe_clock.apps.base import BaseBoxingApp
from boxe_clock.platform.android import actions


class BoxingApp(BaseBoxingApp):
    """The boxing app for Android devices.
    """

    def on_start(self):
        super(BoxingApp, self).on_start()
        actions.keep_screen_on()

    def on_resume(self):
        actions.dim()
