from jnius.jnius import JavaException

try:
    from boxe_clock.platform.android import java
except JavaException:
    def _dummy(*args, **kwargs):
        pass


    vibrate = dim = keep_screen_on = _dummy
else:
    # noinspection PyUnresolvedReferences
    from android.runnable import run_on_ui_thread

    activity = java.PythonActivity.mActivity


    def vibrate(seconds=0.25):
        vibrator = activity.getSystemService(java.Context.VIBRATOR_SERVICE)
        if vibrator.hasVibrator():
            vibrator.vibrate(1000 * seconds)


    @run_on_ui_thread
    def dim():
        view = activity.getWindow().getDecorView()
        view.setSystemUiVisibility(java.View.SYSTEM_UI_FLAG_LOW_PROFILE)


    @run_on_ui_thread
    def keep_screen_on(self):
        activity.getWindow().addFlags(java.Params.FLAG_KEEP_SCREEN_ON)
