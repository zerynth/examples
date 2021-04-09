################################################################################
# Spi
################################################################################


import spi

'''
This spi test works with db zm1 writing on a register
of the spican of EXP SER.
'''

def make_cmd_head(cmd, addr):
    b = bytearray(2)
    b[0] = (cmd) | ((addr>>8) & 0xFF)
    b[1] = addr & 0xFF
    return b

r4b = 48
w4b = 32
reg = 1028

w = make_cmd_head(w4b, reg)
w.append(10)
w.append(9)
w.append(8)
w.append(7)

r_cmd = make_cmd_head(r4b, reg)

can = spi.Spi(10, SPI0, 10000000, spi.SPI_MODE_LOW_FIRST)

sleep(2000)

can.select()
can.write(w)
can.unselect()

can.select()
can.write(r_cmd)

r = can.read(4)
can.unselect()

print("read: ", r[0], r[1], r[2], r[3])

while True:
    sleep(100)