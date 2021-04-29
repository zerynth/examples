import gpio


################################### LEDs UTILS ################################
def set_blue():
    gpio.set(LED_GREEN,1)
    gpio.set(LED_BLUE,0)
    gpio.set(LED_RED,1)  

def set_red():
    gpio.set(LED_GREEN,1)
    gpio.set(LED_BLUE,1)
    gpio.set(LED_RED,0)

def set_green():
    gpio.set(LED_GREEN,0)
    gpio.set(LED_BLUE,1)
    gpio.set(LED_RED,1)

def set_white():
    gpio.set(LED_GREEN,0)
    gpio.set(LED_BLUE,0)
    gpio.set(LED_RED,0)

def set_blink(led, off_pulse, on_pulse):
    gpio.toggle(led)
    sleep(off_pulse)
    gpio.toggle(led)
    sleep(on_pulse)
