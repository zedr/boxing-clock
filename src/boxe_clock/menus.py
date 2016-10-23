from kivy.uix.boxlayout import BoxLayout


class ConfigMenu(BoxLayout):
    def __init__(self, config, **kwargs):
        self.config = config
        super(ConfigMenu, self).__init__(**kwargs)
