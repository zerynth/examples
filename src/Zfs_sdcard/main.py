###############################################################################
# ZFileSystem SD card
################################################################################

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

import fs

while True:
    fs.mount("/sd", fs.SD, 10000000)

    # create a new file and read it back
    f = fs.open("/sd/test.txt","w")
    f.write("first row: test 01\n")
    f.write("second row: test 02\n")
    f.close()

    f = fs.FileIO("/sd/test.txt","r")
    print(f.read())
    f.close()

    fs.unmount("/sd")

    sleep(1000)
