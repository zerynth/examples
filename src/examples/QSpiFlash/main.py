################################################################################
# QSpiFlash Example
#
################################################################################

import qspiflash
import streams

streams.serial()

my_flash = qspiflash.QSpiFlash()

my_flash.erase_block(0)

to_w = b'\x77\x76\x75\x74\x73\x72'
# write data through bracket notation
my_flash[0] = to_w

print("---")

# read 8 bytes starting from 0 address
for x in my_flash.read_data(0, 8):
    print('%02x' % x)

print("---")

# read the same 8 bytes through bracket notation
for x in my_flash[1:1+8]:
    print('%02x' % x)

print("---")

