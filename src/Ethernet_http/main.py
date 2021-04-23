################################################################################
# Ethernet HTTP
################################################################################

#Let's setup an Ethernet connection and use some sockets with HTTP.

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

from networking import eth
from networking import socket

board.init()

while True:
    try:
        # Configure and start ethernet drivers
        print("configuring...")
        eth.configure(dhcp=True)
        print("connecting...")
        eth.start()

        print("connected...")
        print("info...")
        print(eth.info())
        # Get ip of Zerynth
        ip=eth.resolve("now.zerynth.com")
        print("resolved",ip)
        if (ip != None):
            # Open a socket and sent a GET
            print("creating socket...")
            s = socket.socket()
            print("connecting socket...")
            s.connect((ip,80))
            s.send("GET / HTTP/1.1\n")
            s.send("Host: now.zerynth.com\n\n")
            b = s.recv(256)
            print(b)
            print("close socket...")
            s.close()
        # Disconnect
        print("disconnecting...")
        eth.disconnect()
        print("disconnected...")
    except ConnectionError:
        print("Ethernet Connection Exception")
    except ConnectionTimeoutError:
        print("Ethernet Connection Timeout Exception")
    except ResolveError:
        print("Resolv error Exception")
    except NetworkGenericError:
        print("Generic Ethernet Exception")
    except Exception as e:
        raise e

    sleep(3000)
