Sensor driven Multi-Blink
==========================

This examples shows how to drive various behaviours taking as input an analog signal acquired through ADC fro driving three loop implemented as separated threads.
In particular, the implemented scripts drives three LEDs at three different frequencies calculated on the basis of the acquired analog signal.

The example is implemented using 4 threads that run in parallel. One thread is used for acquiring the analog signal and convert the acquired raw value in blinking frequencies usable by the LED driving threads. The other three threads are used to instantiate a generic blinking function that drive a PIN where a LED is connected.

tags:[Multi-Thread, First Steps, Analog Read ADC]
groups:[First Steps]   