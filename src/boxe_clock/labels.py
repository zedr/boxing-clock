from kivy.uix.label import Label

from boxe_clock.mixins import LedMixin


class LedLabel(LedMixin, Label):
    """A LED label.
    """
