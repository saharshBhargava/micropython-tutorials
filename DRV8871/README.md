# Driving DC Motors through DRV8871 on Arduino Giga in MicroPython

## Overview
In this project, a DRV8871 motor driver was used to run a DC motor using an Arduino Giga coded in MicroPython.

## Hardware Timers

The Arduino GIGA R1 has a STM32H747XI processor. There are two advanced-control timers on the board (TIM1, TIM8) which can be used as PWM generators. and they have complementary PWM outputs. 

One set of pins which work for motor control are the PJ6 and PJ7 pins. These pins correspond to the D37 and D38 pins on the Arduino GIGA R1. 

Hardware timers provide precise timing control, ensuring consistent and accurate PWM signal generation. They can also generate PWM signals at much higher frequencies than software-based solutions. Hardware timers ensure a stable and consistent duty cycle and can generate PWM with clean signals. 

Modifying the timer’s frequency can allow for a greater pulse width range. This may be beneficial in cases where a high range of pulse width is needed for precise motor speed control. 

## Determining The Optimal Frequency Using A Logic Analyzer
The pulse width at different frequencies can be measured using a logic analyzer. After determining the optimal frequency and pulse width range using a logic analyzer, the DRV8871 motor driver was used to run a motor. To spin the motor forward, pull the Pin 1 high and then a PWM signal related to the speed you want the motor to spin would be applied to PIN2. 

## Motor & PWM Code
To achieve this, first, lets create a PWM class.

```python

class DualPWM:
    def __init__(self, pin_number, pin_number_n, alt_function, timer, channel_number):
        self.pin = Pin(pin_number, mode=Pin.OUT_PP,value=1)
        self.pin_n = Pin(pin_number_n, mode=Pin.OUT_PP,value=1)
        self.alt_function=alt_function
        self.timer = timer
        self.channel_number=channel_number
        self.channel = self.timer.channel(channel_number, Timer.PWM,  pulse_width_percent=0)

```
We can create various instance variables to store the complementary pair of pins along with the timer and channel we want to use.

Next, we define some functions for our class. 

```python      
    def pulse_width_percent(self, percentage):
        pw = int(24000 * percentage/100) # 24000 was identified as the best PWM width max value for my purpose.
        self.channel.pulse_width(pw) 

    def _stop(self):
        self.pin.init(mode=Pin.OUT_PP,value=1)
        self.pin_n.init(mode=Pin.OUT_PP,value=1)

    def _forward(self,speed):
        self.pin.init(mode = Pin.OUT_PP,value = 1)
        self.pin_n.init( mode = pyb.Pin.ALT, alt = self.alt_function)
        self.pulse_width_percent(100-speed)

    def _reverse(self,speed):
        self.pin_n.init(mode = Pin.OUT_PP, value = 1)
        self.pin.init(mode = pyb.Pin.ALT, alt = self.alt_function)
        self.pulse_width_percent(speed)
```
Next, we can also create a motor class which will help us test out our motor(s).

```python

class Motor:
    def __init__(self, dual_pwm):
        self.dual_pwm = dual_pwm

    def set_speed_percentage(self, speed_percent):
        if speed_percent == 0:
            self.dual_pwm._stop()
            return
        self.dual_pwm._forward(speed_percent)

```
To test the motors, you need to create a timer. The next step would be to create instances of our DualPWM and Motor classes. 

```python

timer = pyb.Timer(8, freq=10000, deadtime=1008)

# Motor Setup
pwm = DualPWM('PJ7','PJ6', alt_function=pyb.Pin.AF3_TIM8, timer=timer, channel_number=2)
motor = Motor(pwm)

```
And finally, simply set the motor's speed percentage to run them as shown below!

```python

# 25% speed
motor.set_speed_percentage(25)
pyb.delay(2000)

# 50% speed
motor.set_speed_percentage(50)
pyb.delay(2000)

# 100% speed
motor.set_speed_percentage(100)
pyb.delay(2000)

motor.set_speed_percentage(0)

```
Thank you for reading!
