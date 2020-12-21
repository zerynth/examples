################################################################################
# Zerynth Time API
#
# Created: 2015-08-17 16:44:58.640097
#
################################################################################

# import streams
import streams
import json

# import the wifi interface
from wireless import wifi

# import the http module
import requests

# the wifi module needs a networking driver to be loaded
# in order to control the board hardware.
# THIS EXAMPLE IS SET TO WORK WITH BCM43362 WIFI DRIVER

# uncomment the following line to use the espressif esp8266 wifi driver (NodeMcu v2, Adafruit Feather Huzzah, Wemos d1 Mini, ...)
# from espressif.esp8266wifi import esp8266wifi as wifi_driver

# uncomment the following line to use the BCM43362 driver (Particle Photon)
from broadcom.bcm43362 import bcm43362 as wifi_driver

# uncomment the following line to use the ESP32 driver (Sparkfun Esp32 Thing, Olimex Esp32, ...)
# from espressif.esp32net import esp32wifi as wifi_driver

streams.serial()

# init the wifi driver!
# The driver automatically registers itself to the wifi interface
# with the correct configuration for the selected board
wifi_driver.auto_init()

# use the wifi interface to link to the Access Point
# change network name, security and password as needed
print("Establishing Link...")
try:
    # FOR THIS EXAMPLE TO WORK, "Network-Name" AND "Wifi-Password" MUST BE SET
    # TO MATCH YOUR ACTUAL NETWORK CONFIGURATION
    wifi.link("Network-Name",wifi.WIFI_WPA2,"Wifi-Password")
except Exception as e:
    print("ooops, something wrong while linking :(", e)
    while True:
        sleep(1000)

## let's try to connect to timeapi.org to get the current UTC time
for i in range(3):
    try:
        print("Trying to connect...")
        # go get that time!
        # url resolution and http protocol handling are hidden inside the requests module
        response = requests.get("http://now.zerynth.com/")
        # let's check the http response status: if different than 200, something went wrong
        print("Http Status:",response.status)
        # if we get here, there has been no exception, exit the loop
        break
    except Exception as e:
        print(e)


try:
    # check status and print the result
    #if response.status==200:
    print("Success!!")
    print("-------------")
    print("And the result is:",response.content)
    print("-------------")
    js = json.loads(response.content)
    print("Date:",js["now"]["rfc2822"][:16])
    print("Time:",js["now"]["rfc2822"][17:])
except Exception as e:
    print("ooops, something very wrong! :(",e)
