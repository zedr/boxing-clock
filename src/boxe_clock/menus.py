from kivy.uix.gridlayout import GridLayout


class ConfigMenu(GridLayout):
    def __init__(self, timer, **kwargs):
        self.timer = timer
        super(ConfigMenu, self).__init__(**kwargs)

