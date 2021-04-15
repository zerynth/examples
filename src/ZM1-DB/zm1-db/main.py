###############################################################################
# ZM1-DB Blink LED
###############################################################################

# Welcome to the simplest ZM1-DB example.
# Let's just loop forever by printing something to the standard output,
# in this case, the USB serial port (open the device console to view the output)
# and blink the green LED

from bsp import board
import gpio

# Initialize the ZM1-DB
board.init()
# Print board information
board.summary()

# loop forever
while True:
    # Print on USB serial port
    print("Blink LED")
    # Blink the green LED
    gpio.toggle(LED_GREEN)
    # sleep 1 second
    sleep(1000)
