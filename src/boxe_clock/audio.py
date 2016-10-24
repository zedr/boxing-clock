import functools


def bell_on_zero(method):
    @functools.wraps(method)
    def inner(self, widget, value):
        if value == 0:
            self.config.bells.current.sound.play()
        return method(self, widget, value)

    return inner
