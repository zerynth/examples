################################################################################
# Zerynth UDP pinger
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

# use the wifi interface to link to the Access Point
# change network name, security and password as needed
print("Establishing Link...")
try:
    # FOR THIS EXAMPLE TO WORK, "Network-Name" AND "Wifi-Password" MUST BE SET
    # TO MATCH YOUR ACTUAL NETWORK CONFIGURATION
    wifi.link("Network-Name",wifi.WIFI_WPA2,"Wifi-Password")
    # get our ip
    myip = wifi.link_info()[0]
    # convert myip to a tuple with the socket.ip_to_tuple function
    # "x.y.z.w" becomes (x,y,z,w)
    ip_tuple = socket.ip_to_tuple(myip)
    # generate a broadcast address to port 9999
    # (it's ok and easier to generate it as a 5 number tuple)
    broadcast = (ip_tuple[0],ip_tuple[1],ip_tuple[2],255,9999)
    print(myip,ip_tuple,broadcast)
    # create an UDP socket and bind it to port 9999
    sock = socket.socket(type=socket.SOCK_DGRAM)
    sock.bind(9999)
except Exception as e:
    print("ooops, something wrong while linking :(", e)
    while True:
        sleep(1000)

        
# this function will be used as a thread
# sending every 2 seconds a message to all
# the udp sockets listening on port 9999 
def ping():
    while True:
        print("Sending")
        sock.sendto("Hello Zerynth!",broadcast)
        sleep(2000)
        
# launch it!
thread(ping)

# in the main thread we listen for incoming udp packets
while True:
    print("Receiving pings")
    try:
        # recvfrom returns both the packet data and the address of the sender
        data,address = sock.recvfrom(32)
        # since we bind to 9999 we also receive the packets we sent
        # check for it by comparing just the ip address (without the port)
        if address[0]!=myip:
            print("Received ping from",address,"=>",str(data))
        else:
            print("Received ping from myself!")
    except Exception as e:
        print(e)
# uplink this script to more than one board and check
