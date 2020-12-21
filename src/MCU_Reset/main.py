###############################################################################
# MCU Reset
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
###############################################################################


# import the mcu module
import mcu
import streams

# open the default serial port, the output will be visible in the serial console
streams.serial()  

resetting = False
# define a simple function to be called on interrupt
def reset():
    global resetting
    resetting=True

# on button pressed, call reset
# >>>> if the board hasn't a button, change BTN0 to a digital pin
#      and use a jumper wire to simulate a falling edge <<<<
onPinFall(BTN0,reset)

# loop forever
while True:
    print("Hello Zerynth!")
    sleep(1000)
    # check for the need to reset
    if resetting:
        print("Resetting in 3 seconds!!")
        sleep(3000)
        mcu.reset()
        # bye!