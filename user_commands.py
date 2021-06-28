import time
from command import Command
from lib.adafruit_hid.keycode import Keycode
from lib.adafruit_hid.consumer_control_code import ConsumerControlCode


def init_user_commands(commands):
    print("Loading user commands")
    # User commands
    # Multiple keypresses at once on the second layer
    commands.add_command(
        command=Command(
            command_list=[(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.LEFT_GUI, Keycode.FOUR)],
            color=(255, 255, 255),
            repeat=False,
            default_color=(50, 50, 50)),
        button=0, layer=0
    )
    commands.add_command(
        command=Command([lambda pixels, kbd, cc: cc.send(ConsumerControlCode.MUTE)], (0, 255, 0), False,
                        (0, 0, 255)), button=12, layer=0)
    commands.add_command(
        command=Command([(Keycode.LEFT_SHIFT, Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.Y)], (0, 122, 55), False,
                        (0, 50, 50)), button=13, layer=0)
    commands.add_command(
        command=Command([lambda pixels, kbd, cc: kbd.send(Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.F5),
                         lambda pixels, kbd, cc: time.sleep(2),
                         lambda pixels, kbd, cc: kbd.send(Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.F1)],
                        (0, 122, 55), False,
                        (50, 50, 0)), button=8, layer=0)
    # Default layer 0
    # commands.add_command(Command(["test", Keycode.ENTER], (255, 0, 0), False, (123, 123, 123)), 0)
    # Can execute a lambda
    # commands.add_command(Command([lambda: print("Console print")], (122, 50, 0), False, (123, 0, 123)), 1)
