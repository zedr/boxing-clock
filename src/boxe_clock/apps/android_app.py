# noinspection PyUnresolvedReferences
from android.runnable import run_on_ui_thread

from boxe_clock.platform.android import java
from boxe_clock.apps.base import BaseBoxingApp


class BoxingApp(BaseBoxingApp):
    """The boxing app for Android devices.
    """

    @run_on_ui_thread
    def keep_screen_on(self):
        java.PythonActivity.mActivity.getWindow().addFlags(
            java.Params.FLAG_KEEP_SCREEN_ON
        )

    @run_on_ui_thread
    def set_systemui_visibility(self, options):
        view = java.PythonActivity.mActivity.getWindow().getDecorView()
        view.setSystemUiVisibility(options)

    @run_on_ui_thread
    def dim(self, *args):
        self.set_systemui_visibility(java.View.SYSTEM_UI_FLAG_LOW_PROFILE)

    def on_start(self):
        super(BoxingApp, self).on_start()
        self.keep_screen_on()
        self.dim()
