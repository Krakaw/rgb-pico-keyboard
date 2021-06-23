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

cs = DigitalInOut(board.GP17)
cs.direction = Direction.OUTPUT
cs.value = 0
num_pixels = 16
pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, num_pixels, brightness=0.1, auto_write=True)
i2c = busio.I2C(board.GP5, board.GP4)
device = I2CDevice(i2c, 0x20)
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)


class Command:
    def __init__(self, command_list, color, repeat=False, default_color=(0, 0, 0)):
        self.repeat = repeat
        self.command_list = command_list
        self.color = color
        self.default_color = default_color

    def process(self):
        for cmd in self.command_list:
            if issubclass(type(cmd), str):
                layout.write(cmd)
            else:
                kbd.send(cmd)


# Add commands for each button
commands = [
    Command(["test", Keycode.ENTER], (255, 0, 0), False, (123, 123, 123))
]

while len(commands) < 16:
    commands.append(False)


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


held = [0] * 16

while True:
    pressed_index = find_pressed_index(0, 16)
    if commands[pressed_index]:
        if not held[pressed_index]:
            pixels[pressed_index] = commands[pressed_index].color
            commands[pressed_index].process()
            if not commands[pressed_index].repeat:
                held[pressed_index] = 1
    else:  # Released state
        for i in range(16):
            if commands[i]:
                pixels[i] = commands[i].default_color
            else:
                pixels[i] = (0, 0, 0)  # Turn pixels off
            held[i] = 0  # Set held states to off
    time.sleep(0.1)  # Debounce
