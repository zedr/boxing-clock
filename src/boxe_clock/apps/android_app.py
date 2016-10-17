from jnius import autoclass

from android.runnable import run_on_ui_thread

from boxe_clock.apps.generic import BoxingApp

PythonActivity = autoclass('org.renpy.android.PythonActivity')
Params = autoclass('android.view.WindowManager$LayoutParams')
View = autoclass('android.view.View')


class AndroidBoxingApp(BoxingApp):
    """The boxing app for Android devices.
    """

    @run_on_ui_thread
    def keep_screen_on(self):
        PythonActivity.mActivity.getWindow().addFlags(
            Params.FLAG_KEEP_SCREEN_ON
        )

    @run_on_ui_thread
    def set_systemui_visibility(self, options):
        PythonActivity.mActivity.getWindow().getDecorView().setSystemUiVisibility(options)

    def dim(self, *args):
        self.set_systemui_visibility(View.SYSTEM_UI_FLAG_LOW_PROFILE)

    def on_start(self):
        super(AndroidBoxingApp, self).on_start()
        self.keep_screen_on()
        self.dim()
