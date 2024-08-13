# Driving DC Motors through DRV8871 on Arduino Giga in MicroPython

The Arduino GIGA R1 has a STM32H747XI processor. There are two advanced-control timers on the board (TIM1, TIM8) which can be used as PWM generators. They have complementary PWM outputs with programmable inserted dead times. Dead times are necessary to prevent short circuits in H-bridges motor drivers as MOSFETs are not perfect.

<img width="624" alt="Screenshot 2024-08-10 at 5 12 25 PM" src="https://github.com/user-attachments/assets/943e7c7c-85a5-4d72-8c99-a0edfaee6e4a">

One set of pins which work for motor control are the PJ6 and PJ7 pins referred to in the image above. These pins correspond to the D37 and D38 pins on the Arduino GIGA R1. The above image was taken from the STM32H747XI processor datasheet.

Hardware timers provide precise timing control, ensuring consistent and accurate PWM signal generation. They can also generate PWM signals at much higher frequencies than software-based solutions. Hardware timers ensure a stable and consistent duty cycle and can generate PWM with clean signals. 

Modifying the timer’s frequency can allow for a greater pulse width range. This may be beneficial in cases where a high range of pulse width is needed for precise motor speed control. The pulse width at different frequencies can be measured using a logic analyzer.

After determining the optimal frequency and pulse width range using a logic analyzer, the DRV8871 motor driver was used to run a motor. To spin the motor forward, pull the Pin 1 high and then a PWM signal related to the speed you want the motor to spin would be applied to PIN2. 

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

Next, we can define some functions for our class. 

```python      
    def pulse_width_percent(self, percentage):
        if percentage > 100:
            percentage = 100
        if percentage < 0:
            percentage =0
        pw = int(24000*percentage/100) # 24000 was identified as the best PWM width max value for my purpose.
        self.channel.pulse_width(pw) 

    def _stop(self):
        self.pin.init(mode=Pin.OUT_PP,value=1)
        self.pin_n.init(mode=Pin.OUT_PP,value=1)

    def _forward(self,speed):
        self.pin.init(mode=Pin.OUT_PP,value=1)
        self.pin_n.init( mode=pyb.Pin.ALT, alt=self.alt_function)
        self.pulse_width_percent(100-speed)

    def _reverse(self,speed):
        self.pin_n.init(mode=Pin.OUT_PP,value=1)
        self.pin.init( mode=pyb.Pin.ALT, alt=self.alt_function)
        self.pulse_width_percent(speed)
```
Next, we can also create a motor class which will help us test out our motor(s).

```python

class Motor:
    def __init__(self, initial_direction, dual_pwm):
        self.direction = initial_direction
        self.dual_pwm = dual_pwm

    def set_speed_percentage(self, speed_percent):
        if speed_percent == 0:
            self.dual_pwm._stop()
            return
        if self.direction == 0:
            self.dual_pwm._reverse(speed_percent)
        else:
            self.dual_pwm._forward(speed_percent)

    def stop(self):
        self.set_speed_percentage(0)

    def set_direction(self,direction):
        self.direction=direction

```

