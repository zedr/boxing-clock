from kivy.app import App
from kivy.uix.label import Label


class MyApp(App):
    def build(self):
        return Label(text=u"Hello world")

def main():
    MyApp().run()


if __name__ == "__main__":
    main()
