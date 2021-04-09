################################################################################
# Zerynth wifi scan
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

# import streams & socket
import streams
import socket

# import the wifi interface
from wireless import wifi

# the wifi module needs a networking driver to be loaded
# in order to control the board hardware.
# FOR THIS EXAMPLE TO WORK, A NETWORK DRIVER MUST BE SELECTED BELOW

# uncomment the following line to use the CC3000 driver (Particle Core or CC3000 Wifi shields)
# from texas.cc3000 import cc3000 as wifi_driver

# uncomment the following line to use the BCM43362 driver (Particle Photon)
# from broadcom.bcm43362 import bcm43362 as wifi_driver

streams.serial()

# init the wifi driver!
# The driver automatically registers itself to the wifi interface
# with the correct configuration for the selected board
wifi_driver.auto_init()

# a list of security strings
wifi_sec=["Open","WEP","WPA","WPA2"]
try:
    print("Scanning for 15 seconds...")
    # start scanning for 15000 milliseconds
    res = wifi.scan(15000)
    
    # if everything goes well, res is a sequence of tuples
    # each tuple contains:
    # -ssid: the name of the network
    # -sec: the security type of the network, from 0 to 3
    # -rssi: the strength of the signal, from 0 to 127
    # -bssid: the mac address of the access point
    for ssid,sec,rssi,bssid in res:
        print(ssid,"::",wifi_sec[sec],":: strength ",rssi*100/127)
except Exception as e:
    print(e)