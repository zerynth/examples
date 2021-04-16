#################################################################################
# RELAY: The Relay library example over a AC circuit with a industrial lamp
#################################################################################

from expansions import relay
from bsp import board
import gpio

# Initialize board
board.init()
# Pass te rotative switch selector position
# address = 0x11
relay_sw_sel = (1,)
# Add the EXP-RELAY to the board
# All pin of the EXP-RELAY will be initialized correctly
exp_relay = board.next_expansion(relay, relay_sw_sel)

while True:
    exp_relay.relay_on(exp_relay.OUT1)
    sleep(3000)
    exp_relay.relay_off(exp_relay.OUT1)