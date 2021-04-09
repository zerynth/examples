################################################################################
# Powersaving
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

##
## This example only works on a Powersaving enabled Virtual Machine!
##

import streams
# import the Power Management module
# Check documentation here: https://docs.zerynth.com/latest/official/core.zerynth.stdlib/docs/official_core.zerynth.stdlib_pwr.html
import pwr

streams.serial()

# wake up reasons dictionary
reasons = {
    pwr.PWR_RESET:"System Reset",
    pwr.PWR_INTERRUPT: "Event on WAKEUP pin",
    pwr.PWR_TIMEOUT: "Timeout"
}

# modes and descriptions
modes = [
    (pwr.PWR_SLEEP, "Sleep mode"),
    (pwr.PWR_STOP, "Stop mode"),
    (pwr.PWR_STANDBY, "Standby mode")
]

# some status variables
slept = 0
wokeup = 0
sleep_counter = 0

# callback for Wake Up events on pins
def wakeup():
    print("Hello!")

# function to prepare for and enter low power mode
def sleepfn(delay,mode):
    global slept,wokeup
    print("Going to sleep for",delay,"milliseconds in",modes[mode][1])
    sleep(100)
    # call go_to_sleep and get the amount of time spent sleeping
    # !! the VM is suspended here !!
    slept = pwr.go_to_sleep(delay,modes[mode][0])
    # if we reach this point, something caused a Wake Up from a low power mode
    # if we don't reach here, the device exited from a standby mode with a system reset

    # retrieve the Wake Up reason
    wokeup = pwr.wakeup_reason()
    print("SLEPT FOR",slept)
    print("My wake up reason:",reasons.get(wokeup,"Unknown"))


try:

    # retrieve the Wake Up reason
    wokeup = pwr.wakeup_reason()
    
    # retrieve sleep_counter from special purpose memory if supported
    try:
        sleep_counter = pwr.get_status_byte(0)
        print("Special purpose memory supported!")
    except Exception as e:
        print("Special purpose memory not supported :(")
    
    # print status at VM startup
    print("Wake up reason at startup:",reasons.get(wokeup,"Unknown"))
    print("Tried to sleep",sleep_counter,"times")

    
    # configure button to do something
    # depending on the platform this is enough to configure a Wake Up event
    # on some platforms only specific pins have the Wake Up property
    # (If the device has no button, configure another pin! [Try D6 on MKR1000 and D8 on Hexiwear])
    pinMode(BTN0,INPUT_PULLUP)
    onPinFall(BTN0, wakeup, debounce=1000)
    
    cnt = 5
    mode = 0
    print("Countdown!")
    while True:
        # print the countdown
        print(cnt)
        sleep(1000)
        
        cnt-=1
        if cnt==0:
            cnt=5
            try:
                # save number of sleeps in special purpose memory
                sleep_counter=(sleep_counter+1)%256
                try:
                    pwr.set_status_byte(0,sleep_counter)
                except:
                    # ignore if special purpose memory not supported
                    pass
                # enter a low power mode for 5 seconds or less
                # (press the button while sleeping to check if Wake Up is available in this mode)
                sleepfn(5000,mode)
            except Exception as e:
                print(modes[mode][1],"not supported!")
                print(e)
            mode=(mode+1)%len(modes)
            print("Countdown!")
except Exception as e:
    print(e)
    
    
# Expected results by architecture and mode for Wake Up on pin event
#
#      MODE  |      SLEEP        STOP                 STANDBY
# MCU        |
# -------------------------------------------------------------------
#            |
# STM32F     |       OK           OK                Only on pin PA0
#            |
# -------------------------------------------------------------------
#            |
# SAMD21     |       OK           No               Mode not supported
#            |
# --------------------------------------------------------------------
#            |
# NXP K64    |       OK           OK               Only on WakeUp pins 
#            |
# --------------------------------------------------------------------
#            |
# ESP8266    |    Unsupported   Unsupported    Only works for Gpio 16
#            |
# --------------------------------------------------------------------


