###############################################################################
# Time
###############################################################################

# All Zerynth boards have a real time clock that helps keeping track of time.

# Let's import the module
import time

# At startup the clock date can be inaccurate, so let's set it now

# create a time info object
tinfo = time.TimeInfo()
tinfo.tm_year = 2021
tinfo.tm_mon = 4
tinfo.tm_mday = 1
tinfo.tm_hour = 17
tinfo.tm_min = 25
tinfo.tm_sec = 35
tinfo.tm_gmtoff = 60

# and use it to set the current time
# Note: the NTP protocol can be used to sync the clock 
# when internet access is available
time.settime(tinfo)

while True:
    # the current unix timestamp can be retrieved in float and integer format
    print("NOW",time.time(),time.now())
    # and the current time can be transformed into a human readable date
    ti = time.localtime()
    print(ti.tm_year, ti.tm_mon, ti.tm_mday, ti.tm_hour, ti.tm_min, ti.tm_sec, ti.tm_gmtoff)
    sleep(1100)

