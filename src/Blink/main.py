###############################################################################
# Led Blink
###############################################################################

# Let's blink some led with threads.

# First, import the board module from the bsp (board support package)
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware without changing a line of code
from bsp import board
# import the gpio control module
import gpio

# Let's define a function to blink a led with some delay
def blink(led, delay):
    while True:
        sleep(delay)
        gpio.toggle(led)


# now let's start two threads, one blinking the blue led
# and one blinking the green led

thread(blink, LED_BLUE, 1000)
thread(blink, LED_GREEN, 2000)

# the two threads are now running independently with different delays.
# the RGB led will turn alternately BLUE and GREEN and CYAN

