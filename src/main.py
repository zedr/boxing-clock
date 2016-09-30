from cerebellum.apps.kivy import KivyApp
from cerebellum.config import configure_kivy


def main():
    configure_kivy()
    KivyApp().run()


if __name__ == "__main__":
    main()
