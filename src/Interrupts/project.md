Interrupt Basics
===================

This example shows how to use interrupts for monitoring pin state changes.
A button is used to connect a pin to ground when pressed. The pin is set as INPUT_PULLUP putting HIGH voltage on it while activated as digital input.
It is possible to use onboard embedded button like in the case of ST Nucleo.
Otherwise an external button can be connected to any digital pin available on the board and then to GND. In this case the pin number have to be changed with the pin used for connecting the button

Note that the main loop (while True) is not present in this example. With ZERYNTH it is possible to write pure event driven code!

tags: [First Steps, Interrupts, Digital I/O]
groups:[First Steps]  
