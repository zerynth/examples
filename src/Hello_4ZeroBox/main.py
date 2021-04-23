###############################################################################
# Hello 4ZeroBox
###############################################################################

# A watchdog resets the board if the firmware hangs. It's a must have for real products.
# A watchdog resets the board after a period of time in which the firmware does not "kick" the watchdog notifying
# that it is working correctly.
import watchdog

# Set watchdog timeout
watchdog.setup(4000)

# loop forever
while True:
    # print something
    print("Hello Zerynth 4ZeroBox!")
    # sleep 1 second
    sleep(1000)
