################################################################################
# struct
#
# Created by Zerynth Team 2017 CC
# Authors: G. Baldi, M. Cipriani
################################################################################

import streams
import struct

streams.serial()

def print_res(b):
    print("Pack -->\n ",end="")
    for x in b:
        print(hex(x,prefix=""),end="")
    print("")

try:
    print("Create pack for 0x01020304 in >xl format")
    b = struct.pack(">xl",0x01020304)
    u = struct.unpack(">xl",b)
    print_res(b)
    print("Unpack -->\n", hex(u[0]))
    print("-------------------------------------------------")
    print("Create pack for a in 10s format")
    b = struct.pack("10s","a")
    u = struct.unpack("10s",b)
    print_res(b)
    print("Unpack -->\n", u[0])
    print("-------------------------------------------------")
    print("Create pack for a in 10p format")
    b = struct.pack("10p","a")
    u = struct.unpack("10p",b)
    print_res(b)
    print("Unpack -->\n", u[0])
    print("-------------------------------------------------")
    print("Create pack for (1,2,3.0) in blf format")
    b = struct.pack("blf",1,2,3.0)
    u = struct.unpack("blf",b)
    print_res(b)
    print("Unpack -->\n", u)
    print("-------------------------------------------------")
    print("Create pack for (-1,9,1.2) in =hlf format")
    b = struct.pack("=hlf",-1,9,1.2)
    u = struct.unpack("=hlf",b)
    print_res(b)
    print("Unpack -->\n", u)
    print("-------------------------------------------------")
    print("Create pack for (127,10,5.5) in =blf format")
    b = struct.pack("=blf",127,10,5.5)
    u = struct.unpack("=blf",b)
    print_res(b)
    print("Unpack -->\n", u)
except Exception as e:
    print(e)

while True:
    print(".")
    sleep(1000)