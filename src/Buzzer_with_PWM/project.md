Buzzer Driven through PWM
==========================
This example shows how to drive a buzzer using PWM. 
In the example a frequency ramp going from 100 Hz to 5 KHz is generated as drive.
The frequency is converted in period to be used as input of the pwm.rite function that require period and pulse to be expressed in milli or micro seconds (measure unit can be selected as extra parameter of the pwm.write function).
The PWM duty cycle is set to 50% driving the buzzer with a symmetric square wave. 

tags:[First Steps, Input Capture Unit ICU, Sound]  
groups:[First Steps]


