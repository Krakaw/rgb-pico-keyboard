import time
from command import Command
from lib.adafruit_hid.keycode import Keycode
from lib.adafruit_hid.consumer_control_code import ConsumerControlCode


def init_user_commands(commands):
    print("Loading user commands")
    # User commands

    # Set audio to headphones
    commands.add_command(
        command=Command([(Keycode.LEFT_SHIFT, Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.H)], (255, 255, 255), False,
                        (0, 200, 0)), button=0, layer=0)

    # Set audio to monitor
    commands.add_command(
        command=Command([(Keycode.LEFT_SHIFT, Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.M)], (255, 255, 255), False,
                        (0, 0, 200)), button=1, layer=0)

    # Mute
    commands.add_command(
        command=Command([lambda pixels, kbd, cc: cc.send(ConsumerControlCode.MUTE)], (0, 255, 0), False,
                        (255, 255, 0)), button=2, layer=0)

    # Screenshot
    commands.add_command(
        command=Command(
            command_list=[(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.LEFT_GUI, Keycode.FOUR)],
            color=(255, 255, 255),
            repeat=False,
            default_color=(50, 50, 50)),
        button=4, layer=0
    )

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
