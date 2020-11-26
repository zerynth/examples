################################################################################
# Watchdogs
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

##
## This example only works on a Secure Firmware enabled Virtual Machine!
##

import streams
# import the Secure Firmware module
# Check documentation here: https://docs.zerynth.com/latest/official/core.zerynth.stdlib/docs/official_core.zerynth.stdlib_sfw.html
import sfw

streams.serial()

sleep(2000)

# Check for reset reason
try:
    print("Watchdog triggered:",sfw.watchdog_triggered())
except Exception as e:
    print("Watchdog not suppported by this Virtual Machine!")
    while True:
        sleep(1000)

# Do something without fearing a reset
for x in range(10):
    sleep(1000)
    print("Printing something for a while, no watchdog can reset me! 8‑D")



# Configure watchdog in normal mode with a 5 seconds timeout
print("Configuring watchdog to a 5 seconds timeout...")
sfw.watchdog(0,5000)
sleep(100)

# Kick the watchdog every second
for x in range(10):
    sleep(1000)
    sfw.kick()
    print("Kick!")
    
# Stop kicking and wait for reset
while True:
    print("Printing something for a while waiting for the watchdog! D-8")
    sleep(1000)
    