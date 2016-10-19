from jnius.jnius import JavaException

try:
    from boxe_clock.platform.android import java
except JavaException:
    def _dummy(*args, **kwargs):
        pass
    vibrate = _dummy
else:
    def vibrate(seconds=0.25):
        activity = java.PythonActivity.mActivity
        vibrator = activity.getSystemService(java.Context.VIBRATOR_SERVICE)
        if vibrator.hasVibrator():
            vibrator.vibrate(1000 * seconds)
