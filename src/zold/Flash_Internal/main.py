################################################################################
# iflash
#
# Created: 2016-03-22 15:54:21.232663
#
################################################################################

import streams
import json
import flash

## Warning! This example works on the Particle Photon only!
# You need to change the flash address to use another board
#  --> For Sam3X based boards you can safely use 0xe0000

streams.serial()


print("create flash file")

# open a 512 bytes FlashFileStream at address 0x80E0000
ff = flash.FlashFileStream(0x80E0000,512)

print("reading flash file")

for i in range(30):
    print(i,"->",str(ff[i]))

print("writing flash file")

sleep(1000)

hh = {
    "type":"thing",
    "data":23.5
}

ds = json.dumps(hh)

# save length and json to flash
ff.write(len(ds))
ff.write(ds)

ff.flush()

ff.seek(0,streams.SEEK_SET)

print("reading flash file")

n = ff.read_int()

for i in range(n+4):
    print(i,"->",str(ff[i]))
