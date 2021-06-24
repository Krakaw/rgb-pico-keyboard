# Adapted from https://gist.github.com/wildestpixel/6b684b8bc886392f7c4c57015fab3d97

import time
import board
import busio
import usb_hid

from adafruit_bus_device.i2c_device import I2CDevice
from lib import adafruit_dotstar

from lib.adafruit_hid.keyboard import Keyboard
from lib.adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from lib.adafruit_hid.keycode import Keycode

from digitalio import DigitalInOut, Direction

# led = DigitalInOut(board.LED)
# led.direction = Direction.OUTPUT
# led.value = True

cs = DigitalInOut(board.GP17)
cs.direction = Direction.OUTPUT
cs.value = 0
num_pixels = 16
pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, num_pixels, brightness=0.1, auto_write=True)
i2c = busio.I2C(board.GP5, board.GP4)
device = I2CDevice(i2c, 0x20)
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

held = [0] * num_pixels


def isalambda(v):
    LAMBDA = lambda: 0
    return isinstance(v, type(LAMBDA))


def colourwheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def find_pressed_index(x, y):
    with device:
        device.write(bytes([0x0]))
        result = bytearray(2)
        device.readinto(result)
        b = result[0] | result[1] << 8
        for i in range(x, y):
            if not (1 << i) & b:
                return i
    return -1


class Commands:
    current_layer = 0
    layer_count = 2
    layer_toggle_button = 15
    use_layer_background = True

    def __init__(self, layer_toggle_button=15, layer_count=2, use_layer_background=True):
        Commands.layer_count = layer_count
        Commands.use_layer_background = use_layer_background
        Commands.layer_toggle_button = layer_toggle_button

        self.commands = []
        for i in range(layer_count):
            self.commands.append([False] * num_pixels)

        self.set_toggle_command()

    def set_toggle_command(self):
        i = 0
        if self.layer_count > 1 and Commands.layer_toggle_button > -1:
            for layer in self.commands:
                layer[Commands.layer_toggle_button] = Command(command_list=[lambda: Commands.increment_layer()],
                                                              color=colourwheel(i),
                                                              default_color=colourwheel(i * num_pixels))
                i = i + 1

    def add_command(self, command, button, layer=0):
        self.commands[layer][button] = command

    def pressed(self, index):
        if index < 0:
            return False

        command = self.commands[Commands.current_layer][index]
        if command:
            if not held[pressed_index]:
                pixels[pressed_index] = command.color
                command.process()
                if not command.repeat:
                    held[pressed_index] = 1
            return True
        return False

    def released(self):
        for i in range(num_pixels):
            if self.commands[self.current_layer][i]:
                pixels[i] = self.commands[self.current_layer][i].default_color
            else:
                if Commands.use_layer_background:
                    pixels[i] = colourwheel(Commands.current_layer * num_pixels)
                else:
                    pixels[i] = (0, 0, 0)  # Turn pixels off
            held[i] = 0  # Set held states to off

    @staticmethod
    def increment_layer():
        Commands.current_layer = (Commands.current_layer + 1) % Commands.layer_count
        commands.released()
        time.sleep(0.5)


class Command:
    def __init__(self, command_list, color, repeat=False, default_color=(0, 0, 0)):
        self.repeat = repeat
        self.command_list = command_list
        self.color = color
        self.default_color = default_color

    def process(self):
        for cmd in self.command_list:
            if isalambda(cmd):
                cmd()
            elif issubclass(type(cmd), str):
                layout.write(cmd)
            else:
                if isinstance(cmd, tuple):
                    kbd.send(*cmd)
                else:
                    kbd.send(cmd)


# ## Edit the commands
# Initialize the commands class
commands = Commands(layer_toggle_button=15, layer_count=2, use_layer_background=True)

# Default layer 0
commands.add_command(Command(["test", Keycode.ENTER], (255, 0, 0), False, (123, 123, 123)), 0)
# Can execute a lambda
commands.add_command(Command([lambda: print("Console print")], (122, 50, 0), False, (123, 0, 123)), 1)
# Multiple keypresses at once on the second layer
commands.add_command(
    command=Command([(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.LEFT_GUI, Keycode.FOUR)], (0, 255, 0), False,
                    (0, 0, 255)), button=0, layer=1)
# ## Stop editing here
# Initialise the keypad
commands.released()

while True:
    pressed_index = find_pressed_index(0, num_pixels)
    if not commands.pressed(pressed_index):
        commands.released()
    time.sleep(0.1)  # Debounce
