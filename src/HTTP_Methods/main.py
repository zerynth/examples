################################################################################
# Zerynth HTTP Methods
#
# Created: 2017-09-19 12:35:25.155721
# Authors: M. Cipriani
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
# THIS EXAMPLE IS SET TO WORK WITH ESP32 WIFI DRIVER

# uncomment the following line to use the espressif esp8266 wifi driver (NodeMcu v2, Adafruit Feather Huzzah, Wemos d1 Mini, ...)
# from espressif.esp8266wifi import esp8266wifi as wifi_driver

# uncomment the following line to use the BCM43362 driver (Particle Photon)
# from broadcom.bcm43362 import bcm43362 as wifi_driver

# uncomment the following line to use the ESP32 driver (Sparkfun Esp32 Thing, Olimex Esp32, ...)
from espressif.esp32net import esp32wifi as wifi_driver

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
    wifi.link("Zerynth",wifi.WIFI_WPA2,"zerynthwifi")
except Exception as e:
    print("ooops, something wrong while linking :(", e)
    while True:
        sleep(1000)

url = "http://httpbin.org/"

tests = [
    {
        "title": "Testing GET Method...",
        "method": requests.get,
        "url": url+"get",
        "params": {"test": "query_string"}
    },
    {
        "title": "Testing POST Method...",
        "method": requests.post,
        "url": url+"post",
        "json": {"test": "json_data"}
    },
    {
        "title": "Testing PUT Method...",
        "method": requests.put,
        "url": url+"put",
        "data": {"test": "urlencoded_data"}
    },
    {
        "title": "Testing PATCH Method...",
        "method": requests.patch,
        "url": url+"patch",
        "data": {"test": "urlencoded_data"}
    },
    {
        "title": "Testing DELETE Method...",
        "method": requests.delete,
        "url": url+"delete",
    },
    {
        "title": "Testing HEAD Method...",
        "method": requests.head,
        "url": url+"get",
    },
    {
        "title": "Testing OPTIONS Method...",
        "method": requests.options,
        "url": url+"get",
    }
]

print("---------------------------------")
for test in tests:
    try:
        print(test["title"])
        if "params" in test:
            response = test["method"](test["url"], params=test["params"])
        elif "json" in test:
            response = test["method"](test["url"], json=test["json"])
        elif "data" in test:
            response = test["method"](test["url"], data=test["data"])
        else:
            response = test["method"](test["url"])
        print("Http Status:",response.status)
        print("Http Headers:",response.headers)
        print("Http Content:",response.content)
        print("---------------------------------")
        response = None
    except Exception as e:
        print(e)
    sleep(2000)