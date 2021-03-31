###############################################################################
# EXP-RELAY
###############################################################################

# Welcome to EXP-RELAY example.
# Let's see how to initialize and use outputs relay of the EXP-RELAY

from expansions import relay
from bsp import board
import gpio

# Initialize ZM1-DB
board.init()
# Pass te rotative switch selector position
# address = 0x11
relay_sw_sel = (1,)
# Add the EXP-RELAY to the ZM1-DB
# All pin of the EXP-RELAY will be initialized correctly
exp_relay = board.next_expansion(relay, relay_sw_sel)

# Use gpio api to control EXP-RELAY Outputs
gpio.high(exp_relay.OUT1)
gpio.low(exp_relay.OUT2)
while True:
    # Switch outputs logic value
    gpio.toggle(exp_relay.OUT1)
    gpio.toggle(exp_relay.OUT2)
    # sleep 1 second
    sleep(1000)
