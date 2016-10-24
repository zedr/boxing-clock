from boxe_clock.config import TimerConfig


class LedMixin(object):
    """A mixing for widgets that use the LED-inspired font.
    """
    font_name = TimerConfig.fonts("digital")
