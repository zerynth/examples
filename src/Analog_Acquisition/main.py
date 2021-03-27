################################################################################
# Analog Read
################################################################################

# let's read some analog values from a gpio

# First, import the board module from the bsp (board support package)
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware without changing a line of code
from bsp import board
# import the adc module
import adc


# loop forever
while True:
    # acquiring the analog signal from a pin
    value = adc.read(A0) 
    # convert to range [0..80]
    conv = value*80//4095
    print("|","#"*conv," "*(80-conv),"|",value)
    sleep(300)
