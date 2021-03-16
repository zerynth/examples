################################################################################
# SpiFlash Example
#
# Created: 2016-04-21 19:16:44.440555
#
################################################################################

import spiflash
import streams

streams.serial()


my_flash = spiflash.SpiFlash(SPI0, D25)

my_flash.erase_sector(0x30122)

to_w = [235,166,128,124,65,66]
# write data through bracket notation
my_flash[0x30122] = to_w

print("---")

# read 8 bytes starting from 0x30122 address
for x in my_flash.read_data(0x30122,8):
    print(x)

print("---")

# read the same 8 bytes through bracket notation
for x in my_flash[0x30123:0x30123+8]:
    print(x)

print("---")
