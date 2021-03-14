Interrupt Advanced
===================

This example uses pwm to show the advanced feature of interrupt debouncing.
PWM triggers fall and rise events at different speeds, but interrupts are triggered only if the debounce time (i.e. the stable time after and event) is in the correct range.