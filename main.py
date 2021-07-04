import microcontroller
import time
import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice
from user_commands import init_user_commands
from command import Command, pixels, num_pixels

temperature_button = -1  # Set to -1 to disable
temp_aggregate = []

i2c = busio.I2C(board.GP5, board.GP4)
device = I2CDevice(i2c, 0x20)

# Key currently being held down
held = [0] * num_pixels
# State of key if it has been toggled (allow for on/off states) only 1 key can be toggled at a time
toggled_key = -1


def relative_color(max_rgb=(255, 255, 255), direction=(1, 1, 1), min_max_values=(0, 100), value=0):
    """
    Returns the relative color in a range
    :param max_rgb:
    :param direction:
    :param min_max_values:
    :param value:
    :return:
    """
    clean_value = max(min(min_max_values[1], value), min_max_values[0])
    normalized_percent = (clean_value - min_max_values[0]) / (min_max_values[1] - min_max_values[0])

    r = round(max_rgb[0] * normalized_percent)
    r = (r, max_rgb[0] - r)[direction[0] == 1]
    g = round(max_rgb[1] * normalized_percent)
    g = (g, max_rgb[1] - g)[direction[1] == 1]
    b = round(max_rgb[2] * normalized_percent)
    b = (b, max_rgb[2] - b)[direction[2] == 1]
    return (r, g, b)


def colourwheel(pos, offset=(0, 0, 0)):
    pos = pos % 255
    r = offset[0]
    g = offset[1]
    b = offset[2]
    if pos < 85:
        return ((255 - pos * 3) - r, (pos * 3) + g, 0 + b)
    if pos < 170:
        pos -= 85
        return (0 + r, (255 - pos * 3) - g, (pos * 3) + b)
    pos -= 170
    return ((pos * 3) + r, 0 + g, (255 - pos * 3) - b)


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

        self.set_toggle_layer_command()

    def set_toggle_layer_command(self):
        i = 0
        if self.layer_count > 1 and Commands.layer_toggle_button > -1:
            for layer in self.commands:
                default_color = colourwheel(i * num_pixels, offset=(15, 15, 15))
                layer[Commands.layer_toggle_button] = Command(
                    command_list=[lambda pixels, kbd, cc: Commands.increment_layer()],
                    color=colourwheel(i * num_pixels * 2),
                    default_color=default_color)
                i = i + 1

    def add_command(self, command, button, layer=0):
        self.commands[layer][button] = command

    def pressed(self, index, toggle=False):
        global toggled_key
        if index < 0:
            return False

        command = self.commands[Commands.current_layer][index]
        if command:
            if command.stay_pressed and (toggle or toggled_key == -1):
                if toggled_key != index:
                    toggled_key = index
                else:
                    toggled_key = -1
                    # Debounce multiple key presses
                    time.sleep(0.3)

            if not held[index]:
                pixels[index] = command.color
                command.process()
                if not command.repeat:
                    held[index] = 1
            return True
        return False

    def released(self):
        for i in range(num_pixels):
            if -1 < temperature_button == i:
                continue
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
        time.sleep(0.25)


# ## Edit the commands
# Initialize the commands class
commands = Commands(layer_toggle_button=15, layer_count=2, use_layer_background=True)

init_user_commands(commands)

# ## Stop editing here
# Initialise the keypad
commands.released()

while True:
    pressed_index = find_pressed_index(0, num_pixels)
    toggle = False
    if toggled_key > -1:
        toggle = pressed_index == toggled_key
        pressed_index = toggled_key

    if not commands.pressed(pressed_index, toggle):
        commands.released()
    time.sleep(0.1)  # Debounce
    if temperature_button > -1:
        temp = microcontroller.cpu.temperature
        if len(temp_aggregate) < 10:
            temp_aggregate.append(temp)
        else:
            avg_temp = sum(temp_aggregate) / len(temp_aggregate)
            temp_aggregate = []
            pixels[temperature_button] = relative_color((255, 0, 255), (-1, 1, 1), (10, 30), avg_temp)
