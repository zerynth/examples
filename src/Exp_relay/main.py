#################################################################################
# RELAY: The Relay library example over a AC circuit with a industrial lamp
#################################################################################

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board
from expansions import relay
import gpio

def turn_lamp_on(exp, out):
    exp.relay_on(out)

def turn_lamp_off(exp, out):
    exp.relay_off(out)


# Initialize board
board.init()
# Pass te rotative switch selector position
# address = 0x11
relay_sw_sel = (1,)
# Add the EXP-RELAY to the board
# All pin of the EXP-RELAY will be initialized correctly
exp_relay = board.next_expansion(relay, relay_sw_sel)
rel1 = exp_relay.OUT1
# Use gpio api to turn the lamp on and off
while True:
    # Switch relay state
    if exp_relay.is_relay_on(rel1):
        turn_lamp_off(exp_relay, rel1)
    else:
        turn_lamp_on(exp_relay, rel1)
    # Sleep 3 seconds
    sleep(3000)
