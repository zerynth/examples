################################################################################
# Watchdogs
################################################################################

# A watchdog resets the board if the firmware hangs. It's a must have for real products.
# A watchdog resets the board after a period of time in which the firmware does not "kick" the watchdog notifying
# that it is working correctly.
# In Zerynth the watchdog is configured BEFORE the firmware starts and can be reconfigured in the firmware.
# The initial time window of the watchdog is define in the config.yml with the ZERYNTH_EARLY_WATCHDOG variable.
import watchdog
import mcu

# Firmware is starting, let's check if the last reset was due to a triggered watchdog
print("Watchdog triggered:",mcu.reset_reason() == mcu.RESET_WATCHDOG)

# Watchdog is enabled in config.yml with a 5 seconds window
# Let's do something for a while without fearing a reset
for x in range(3):
    sleep(1000)
    print("Printing something for a while, no watchdog can reset me! 8‑D")

# Kick the watchdog every second
for x in range(10):
    watchdog.kick()
    print("Kick!")
    sleep(1000)

# Stop kicking and wait for reset
while True:
    print("Printing something for a while waiting for the watchdog! D-8")
    sleep(1000)

