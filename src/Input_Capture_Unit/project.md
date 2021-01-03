Input Capture Unit as PWM Analyzer
===================================

This examples shows how to use the Input Capture Unit of the board MCU for analysing a PWM signal 
The PWM is generated on PIN13 in order to have a feedbakc on the board embedded LED
PIN13 is also connected through a wire with PIN2 on which the ICU capture is activated
An interrupt is also attached on a PIN where a button is connected for changing the PWM duty.

Very Important: ICU and PWM are both timer powered embedded feature, it is impossible to run an ICU and a PWM
on two pin controlled by the same timer channel. 
Please refer to the board pinout in order to select the proper pins for your board
e.i: on a ST Nucleo this example use PWM2/1 for PIN13 and PWM1/3 for PIN2 so we are using two diferent embedded timers (first number on the PEM pin descrition)

Board setup:   
  PIN13-----PIN2  (shortcut the pins)
  BTNPin----GND   (connect a button between a pin and GND)  

tags: [First Steps, Input Capture Unit ICU, Interrupts, Analog Write PWM]  
groups:[First Steps]


