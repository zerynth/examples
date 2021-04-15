################################################################################
# SpiSD Example
#
# Created: 2016-04-29 12:37:53.316436
#
################################################################################

import spisd
import streams

streams.serial()


my_sd = spisd.SpiSD(SPI0, D25)
data = bytearray(512*2)
for i in range(512*2):
    data[i] = 166

# write 512 bytes of data starting from 3rd block
my_sd.write_data(3,data)

# read 512*3 bytes of data starting from 3rd block
for i, x in enumerate(my_sd.read_data(3,3)):
    print(hex(0x200*3+i),": ",x)
