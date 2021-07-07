import time
from command import Command
from lib.adafruit_hid.keycode import Keycode
from lib.adafruit_hid.consumer_control_code import ConsumerControlCode


def init_user_commands(commands):
    print("Loading user commands")
    # User commands

    # Set audio to headphones
    commands.add_command(
        command=Command([(Keycode.LEFT_SHIFT, Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.H)], (255, 255, 255),
                        False,
                        (0, 100, 0)), button=0, layer=0)

    # Set audio to monitor
    commands.add_command(
        command=Command([(Keycode.LEFT_SHIFT, Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.M)], (255, 255, 255),
                        False,
                        (0, 100, 0)), button=1, layer=0)

    # Volume Down
    commands.add_command(
        command=Command([lambda pixels, kbd, cc: cc.send(ConsumerControlCode.VOLUME_DECREMENT)], (0, 0, 255), True,
                        (50, 150, 0)), button=2, layer=0)

    # Volume Up
    commands.add_command(
        command=Command([lambda pixels, kbd, cc: cc.send(ConsumerControlCode.VOLUME_INCREMENT)], (255, 0, 0), True,
                        (50, 200, 0)), button=3, layer=0)

    # Mute
    commands.add_command(
        command=Command([lambda pixels, kbd, cc: cc.send(ConsumerControlCode.MUTE)], (0, 255, 0), False,
                        (50, 100, 0)), button=6, layer=0)

    # Push To Talk
    commands.add_command(
        command=Command(command_list=[(Keycode.LEFT_SHIFT, Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.F1)],
                        color=(0, 255, 0), repeat=True,
                        default_color=(0, 25, 0), stay_pressed=True), button=7, layer=0)

    # Screenshot
    commands.add_command(
        command=Command(
            command_list=[(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.LEFT_GUI, Keycode.FOUR)],
            color=(255, 255, 255),
            repeat=False,
            default_color=(50, 50, 50)),
        button=4, layer=0
    )

    # Move screen to corners
    # Move screen to top
    commands.add_command(
        command=Command(
            command_list=[(Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.LEFT_GUI, Keycode.KEYPAD_EIGHT)],
            color=(255, 255, 0),
            repeat=False,
            default_color=(255, 50, 0)),
        button=5, layer=0
    )

    # Move screen to left
    commands.add_command(
        command=Command(
            command_list=[(Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.LEFT_GUI, Keycode.KEYPAD_FOUR)],
            color=(255, 255, 0),
            repeat=False,
            default_color=(255, 50, 0)),
        button=8, layer=0
    )

    # Move screen to bottom
    commands.add_command(
        command=Command(
            command_list=[(Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.LEFT_GUI, Keycode.KEYPAD_TWO)],
            color=(255, 255, 0),
            repeat=False,
            default_color=(255, 50, 0)),
        button=9, layer=0
    )

    # Move screen to right
    commands.add_command(
        command=Command(
            command_list=[(Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.LEFT_GUI, Keycode.KEYPAD_SIX)],
            color=(255, 255, 0),
            repeat=False,
            default_color=(255, 50, 0)),
        button=10, layer=0
    )

    # Open terminal
    commands.add_command(
        command=Command(
            [lambda p, k, c: k.send(Keycode.LEFT_CONTROL, Keycode.GRAVE_ACCENT), lambda p, k, c: time.sleep(0.3)],
            (255, 255, 0), True,
            (50, 50, 0)), button=11, layer=0)

    # Raise windows
    commands.add_command(
        command=Command([(Keycode.LEFT_SHIFT, Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.Z)], (0, 122, 55), False,
                        (0, 50, 50)), button=13, layer=0)

    # Minimize windows
    commands.add_command(
        command=Command([(Keycode.LEFT_SHIFT, Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.Y)], (0, 122, 55), False,
                        (0, 50, 50)), button=14, layer=0)

    # Swap to terminal and back
    commands.add_command(
        command=Command([lambda pixels, kbd, cc: kbd.send(Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.F5),
                         lambda pixels, kbd, cc: time.sleep(2),
                         lambda pixels, kbd, cc: kbd.send(Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.F1)],
                        (0, 122, 55), False,
                        (50, 50, 0)), button=12, layer=0)
    # Default layer 0
    # commands.add_command(Command(["test", Keycode.ENTER], (255, 0, 0), False, (123, 123, 123)), 0)
    # Can execute a lambda
    # commands.add_command(Command([lambda: print("Console print")], (122, 50, 0), False, (123, 0, 123)), 1)
