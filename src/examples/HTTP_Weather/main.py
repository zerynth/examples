################################################################################
# Zerynth Weather
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################



# import streams & socket
import streams
import socket

# import json parser, will be needed later
import json

# import the wifi interface
from wireless import wifi

# import the http module
import requests

# the wifi module needs a networking driver to be loaded
# in order to control the board hardware.
# THIS EXAMPLE IS SET TO WORK WITH ESP8266 WIFI DRIVER

# uncomment the following line to use the espressif esp8266 wifi driver (NodeMcu v2, Adafruit Feather Huzzah, Wemos d1 Mini, ...)
from espressif.esp8266wifi import esp8266wifi as wifi_driver

# uncomment the following line to use the BCM43362 driver (Particle Photon)
# from broadcom.bcm43362 import bcm43362 as wifi_driver

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

# let's try to connect to openweathermap.org to get some weather info
# for this example to work you need a openweathermap API key
# if you don't have one, you can get one for free here: http://openweathermap.org/price

# type here your API key!
# or you can use ours...however, if our calls quota is exceded 
# the example won't work :(
api_key = "bd4ba90e2b397e24a925e436a9d8fed9"
        
for i in range(3):
    try:
        print("Trying to connect...")
        # to get weather info you need to specify a correct api url
        # there are a lot of different urls with different functions
        # they are all documented here http://openweathermap.org/api
        
        # let's put the http query parameters in a dict
        params = {
            "APPID":api_key,
            "q":"Pisa"   # <----- here it goes your city
        }
        
        # the following url gets weather information in json based on the name of the city
        url="http://api.openweathermap.org/data/2.5/weather"
        # url resolution and http protocol handling are hidden inside the requests module
        response = requests.get(url,params=params)
        # if we get here, there has been no exception, exit the loop
        break
    except Exception as e:
        print(e)


try:
    # check status and print the result
    if response.status==200:
        print("Success!!")
        print("-------------")
        # it's time to parse the json response
        js = json.loads(response.content)
        # super easy!
        print("Weather:",js["weather"][0]["description"],js["main"]["temp"]-273,"degrees")
        print("-------------")
except Exception as e:
    print("ooops, something very wrong! :(",e)



