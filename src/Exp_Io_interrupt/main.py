###############################################################################
# EXP-IO: Interrupt on opto-isolated
###############################################################################

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

from expansions import io
import gpio

# Initialize board
board.init()

# Pass the rotative switch selector position
# address = 0x11, interrupt = INTR
io_sw_sel = (1, 0,)

# Add the EXP-IO to the board
# All pin of the EXP-IO will be initialized correctly
exp_io = board.next_expansion(io, io_sw_sel)

def riseFunction():
    print("increasing value")

def fallFunction():
    print("decreasing value")

gpio.on_rise(exp_io.DIN1, riseFunction)
gpio.on_fall(exp_io.DIN1, fallFunction)

while True:
    # Switch logic value
    gpio.toggle(exp_io.DIN1)
    print("DIN1 =", gpio.get(exp_io.DIN1))
    sleep(3000)
