###############################################################################
# EXP-SER: RS232
###############################################################################

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

from expansions import ser
import can
import msg_exchange
import gpio

tx_ch = 1
tx_prio = 1
rx_ch = 2
q_size = 5

# Initialize board
board.init()
# Pass the rotative switch selector position
# Interrupt pin INTR
ser_sw_sel = (0,)
# Add the EXP-SER to the board
# All pin of the EXP-SER will be initialized correctly
exp_ser = board.next_expansion(ser, ser_sw_sel)
# Initialize get initialized can from EXP-SER
# CAN controlled by CTS1
exp_can = exp_ser.get_can(CTS1, spi_clk=10000000)

# Configure can channels
exp_can.conf()
exp_can.txf_conf(tx_ch, q_size, tx_prio)
exp_can.rxf_conf(rx_ch, q_size)
# Start can
exp_can.start()

# Add filter on rx (required)
filter_n = 1
exp_can.add_filter(filter_n, rx_ch, 0x300, 0x7F0)

# Init alert pin on RX
gpio.mode(INTR, INPUT_PULLUP)
exp_can.en_rx_intr(rx_ch)

while True:
    # From msg_exchange call the ping_starter function on one board
    # and ping_receiver on the other to start a PING-PONG between the two.

    # Uncomment to create the PING sender
    msg_exchange.ping_starter(exp_can, tx_ch, rx_ch)

    # Uncomment to create the PING receiver
    # msg_exchange.ping_receiver(exp_can, tx_ch, rx_ch)
