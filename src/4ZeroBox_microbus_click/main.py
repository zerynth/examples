###############################################################################
# 4ZeroBox microbus click
################################################################################

import i2c
from components.bme280 import bme280

sens = bme280.BME280(I2C0)

while True:
    thp = sens.get_values_fast()
    print(thp)
    t = sens.get_temp()
    print("temperature: ", t)
    h = sens.get_hum()
    print("humidity: ", h)
    p = sens.get_press()
    print("pressure: ", p)
    sleep(1000)