###############################################################################
# EXP-IO: Interrupt on opto-isolated
###############################################################################

from expansions import io
from bsp import board
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