################################################################################
# Interrupts
################################################################################

from bsp import board
import gpio


touches = 0
button = USER_BUTTON

# Let's define a function that will be called when the button changes state
# The gpio and the value of the gpio are passed to the function by the system
def on_touch(pin, value):
    global touches
    if value != 0:
        touches += 1
        print("touched",touches,"times")

# Let's attach the function to the user button.
# Also, set a debounce: an event is generated only if the new state of the button
# is maintained for a period of time (300 millis). This avoid spurious state changes
# and noise.
gpio.on_rise(USER_BUTTON,on_touch,debounce=300)


# Wait forever for the button to be pressed
while True:
    sleep(1000)
