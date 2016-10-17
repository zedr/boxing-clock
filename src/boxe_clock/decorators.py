def bell_enabled(method):
    def inner(self, widget, value):
        if value == 0:
            self.bell_sound.play()
        return method(self, widget, value)

    return inner
