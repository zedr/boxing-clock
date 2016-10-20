try:
    from boxe_clock.apps.android_app import BoxingApp
except ImportError:
    from boxe_clock.apps.generic_app import BoxingApp


def main():
    BoxingApp().run()


if __name__ == "__main__":
    main()
