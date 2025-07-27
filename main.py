import time
import board
import busio
import usb_hid
import random

from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_dotstar
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from array import *

# configure i2c keypad
from digitalio import DigitalInOut, Direction, Pull

cs = DigitalInOut(board.GP17)
cs.direction = Direction.OUTPUT
cs.value = 0
num_pixels = 16
pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, num_pixels, brightness=0.1, auto_write=True)
i2c = busio.I2C(board.GP5, board.GP4)
device = I2CDevice(i2c, 0x20)
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)


# program functions
def read_button_states(x, y):
    pressed = [0] * 16
    with device:
        device.write(bytes([0x0]))
        result = bytearray(2)
        device.readinto(result)
        b = result[0] | result[1] << 8
        for i in range(x, y):
            if not (1 << i) & b:
                pressed[i] = 1
            else:
                pressed[i] = 0
    return pressed


def toggle(this):
    if this == 1:
        val = 0
    else:
        val = 1
    return val


def debounce(amount):
    time.sleep(amount)  # just wait a bit for the pressed signals to settle down


def handle_led(ID, colour):
    latch[ID] = toggle(latch[ID])  # toggle the latch
    if latch[ID] == 1:
        pixels[ID] = colour  # Map pixel index to 0-255 range
    else:
        pixels[ID] = _base


def set_set(set_id):
    latch[set_id] = 1  # set the key to latched
    pixels[set_id] = _pink  # set control set led to green
    for i in range(4):
        if i != set_id:
            pixels[i] = (0, 0, 0)
            latch[i] = 0

    # set all defined keys in the set to the base colour
    # keys not defined are set to off 0,0,0
    for i in range(4, 16):
        if button_set[i + (set_id * 16)][0] == "empty":
            pixels[i] = (0, 0, 0)
        else:
            pixels[i] = _base


def startup(base_colour):
    for i in range(16):
        if i < 4:
            pixels[i] = _pink  # color selector keys start as
        else:
            pixels[i] = (0, 0, 0)


def send_keycodes(k, x):
    codes = button_set[x][0]  # codes to send
    # print(codes)
    latch = button_set[x][2]  # latch boolean 1 or 0
    col = button_set[x][3]  # get the colour
    handle_led(k, col)  # set the led to the correct colour
    # split on comma
    symbols = codes.split(",")
    # print(symbols)
    if len(symbols) == 3:
        kbd.send(eval(symbols[0]), eval(symbols[1]), eval(symbols[2]))
    else:
        kbd.send(eval(symbols[0]), eval(symbols[1]))


def send_text(k, x):
    text = button_set[x][0]  # text to send
    col = button_set[x][3]  # get the colour
    handle_led(k, col)  # set the led to the correct colour
    if text == "_random_":
        r = random.randint(0, l)
        text = messages[r]

    layout.write(text)  # send the text
    kbd.send(Keycode.ENTER)  # send enter


# ---- define colours ----
_red = (255, 0, 0)
_green = (0, 255, 0)
_blue = (0, 0, 255)
_yellow = (255, 255, 0)
_orange = (255, 103, 0)
_purple = (84, 22, 250)
_base = (255, 103, 0)  # colour to light the key if it defined
_black = (0, 0, 0)
_pink = (247, 0, 255)

# ---- define button set array ----
button_set = {}
for i in range(64):
    button_set[i] = ["empty", 0, 0, _red]

# ---- 1ST - SHOW SOFTWARE ---- 4 - 15
# (keycodes or text , flag 0=kc 1=text, latch flag 0=no 1=yes, colour)
button_set[4] = ["Keycode.CONTROL,Keycode.SHIFT,Keycode.S", 0, 0, _purple]  # open ATEM + OBS
button_set[12] = ["Keycode.CONTROL,Keycode.SHIFT,Keycode.O", 0, 0, _blue]  # open OBS
button_set[8] = ["Keycode.CONTROL,Keycode.SHIFT,Keycode.A", 0, 0, _red]  # open ATEM

button_set[13] = ["Keycode.SHIFT,Keycode.COMMAND,Keycode.R", 0, 0, _green]  # Start recoding
button_set[14] = ["Keycode.ALT,Keycode.SHIFT,Keycode.R", 0, 0, _red]  # stop recording

# ---- 2nd - Daily Applications ---- 20 - 31
button_set[20] = ["Keycode.SHIFT,Keycode.COMMAND,Keycode.F", 0, 0, _purple]  # open Firefox

button_set[28] = ["Keycode.SHIFT,Keycode.COMMAND,Keycode.P", 0, 0, _yellow]  # open pycharm
button_set[29] = ["Keycode.SHIFT,Keycode.COMMAND,Keycode.T", 0, 0, _blue]  # open thonny
button_set[30] = ["Keycode.SHIFT,Keycode.COMMAND,Keycode.M", 0, 0, _orange]  # open Mu editor

# ---- 3rd - Music Control ---- 36 - 47
button_set[36] = ["Keycode.CONTROL,Keycode.SHIFT,Keycode.M", 0, 0, _purple]  # open music

button_set[38] = ["Keycode.CONTROL,Keycode.SHIFT,Keycode.F", 0, 0, _blue]  # next song
button_set[42] = ["Keycode.ALT,Keycode.SHIFT,Keycode.F", 0, 0, _blue]  # previous song

button_set[39] = ["Keycode.CONTROL,Keycode.SHIFT,Keycode.V", 0, 0, _green]  # play music
button_set[43] = ["Keycode.CONTROL,Keycode.SHIFT,Keycode.W", 0, 0, _red]  # pause music

button_set[46] = ["Keycode.COMMAND,Keycode.UP_ARROW", 0, 0, _red]  # raise volume while app selected
button_set[47] = ["Keycode.COMMAND,Keycode.DOWN_ARROW", 0, 0, _green]  # lowers volume while app selected

button_set[44] = ["Keycode.CONTROL,Keycode.SHIFT,Keycode.TAB", 0, 0, _blue]
button_set[40] = ["Keycode.ALT,Keycode.SHIFT,Keycode.I", 0, 0, _pink]
button_set[41] = ["Keycode.CONTROL,Keycode.SHIFT,Keycode.B", 0, 0, _green]
# ---- 4th - UNASSIGNED ---- 52 - 63


# ---- Variable setup ---- #
held = [0] * 16  # setup
latch = [0] * 16  # setup
_set = 5  # set the default active button set to > 4 so i.e. no active set!
todo = False
l = len(messages) - 1  # number of random messages we have to choose from

# ---- Main programme starts here -----
startup(_base)  # light up the top row with the base colour as the keys are defined

# ---- main loop starts here ---- #
while True:
    pressed = read_button_states(0, 16)

    if pressed[0]:
        _set = 0
        set_set(_set)
        debounce(0.25)  # debounce
        kbd.release_all()
        debounce(0.4)
        held = [0] * 16  # setup
        latch = [0] * 16  # setup
        held[_set] = 1

    elif pressed[1]:
        _set = 1
        set_set(_set)
        debounce(0.25)  # debounce
        kbd.release_all()
        debounce(0.4)
        held = [0] * 16  # setup
        latch = [0] * 16  # setup
        held[_set] = 1

    elif pressed[2]:
        _set = 2
        set_set(_set)
        debounce(0.25)  # debounce
        kbd.release_all()
        debounce(0.4)
        held = [0] * 16  # setup
        latch = [0] * 16  # setup
        held[_set] = 1

    elif pressed[3]:
        _set = 3
        set_set(_set)
        debounce(0.25)  # debounce
        kbd.release_all()
        debounce(0.4)
        held = [0] * 16  # setup
        latch = [0] * 16  # setup
        held[_set] = 1

    else:
        for i in range(4, 16):
            if pressed[i] and button_set[i + (_set * 16)][0] != "empty":
                # if we get here we have something to do.
                todo = True
                index = i + (_set * 16)
                if not held[i]:
                    if button_set[index][1] == 0:
                        send_keycodes(i, index)  # call the function to send keycodes
                        debounce(0.25)
                    else:
                        send_text(i, index)  # call the function to send text
                        debounce(0.25)
                        pixels[i] = _base  # because this is sending text we do not latch the led
                        latch[i] = 0

                kbd.release_all()
                held[i] = 1
                debounce(0.4)
                if button_set[index][2] == 0:  # if the button shouuld not latch
                    pixels[i] = _base  # set LEDS back to base colour
        if todo:
            for i in range(16):
                held[i] = 0  # Set held states to off
            todo = False
