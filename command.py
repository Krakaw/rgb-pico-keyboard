import board
import usb_hid

from lib import adafruit_dotstar

from lib.adafruit_hid.keyboard import Keyboard
from lib.adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from lib.adafruit_hid.consumer_control import ConsumerControl
from digitalio import DigitalInOut, Direction

cs = DigitalInOut(board.GP17)
cs.direction = Direction.OUTPUT
cs.value = 0
num_pixels = 16
pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, num_pixels, brightness=0.1, auto_write=True)
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

layout = KeyboardLayoutUS(kbd)


def isalambda(v):
    LAMBDA = lambda: 0
    return isinstance(v, type(LAMBDA))


class Command:
    def __init__(self, command_list, color, repeat=False, default_color=(0, 0, 0)):
        self.repeat = repeat
        self.command_list = command_list
        self.color = color
        self.default_color = default_color

    def process(self):
        for cmd in self.command_list:
            if isalambda(cmd):
                cmd(pixels, kbd, cc)
            elif issubclass(type(cmd), str):
                layout.write(cmd)
            else:
                if isinstance(cmd, tuple):
                    kbd.send(*cmd)
                else:
                    kbd.send(cmd)
