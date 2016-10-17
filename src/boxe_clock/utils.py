from boxe_clock.constants import Colors


def format_time(seconds, color=Colors.WHITE):
    return "[color={0}]{1}:{2:02d}[/color]".format(
        color,
        seconds // 60,
        seconds % 60
    )
