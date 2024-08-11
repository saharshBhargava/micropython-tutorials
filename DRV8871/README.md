# Driving DC Motors through DRV8871 on Arduino Giga in MicroPython

The Arduino GIGA R1 has a STM32H747XI processor. There are two advanced-control timers on the board (TIM1, TIM8) which can be used as PWM generators. They have complementary PWM outputs with programmable inserted dead times. Dead times are necessary to prevent short circuits in H-bridges motor drivers as MOSFETs are not perfect.

<img width="624" alt="Screenshot 2024-08-10 at 5 12 25 PM" src="https://github.com/user-attachments/assets/943e7c7c-85a5-4d72-8c99-a0edfaee6e4a">

One set of pins which work for motor control are the PJ6 and PJ7 pins referred to in the image above. These pins correspond to the D37 and D38 pins on the Arduino GIGA R1. The above image was taken from the STM32H747XI processor datasheet.

Hardware timers provide precise timing control, ensuring consistent and accurate PWM signal generation. They can also generate PWM signals at much higher frequencies than software-based solutions. Hardware timers ensure a stable and consistent duty cycle and can generate PWM with clean signals. 

Modifying the timer’s frequency can allow for a greater pulse width range. This may be beneficial in cases where a high range of pulse width is needed for precise motor speed control. The pulse width at different frequencies can be measured using a logic analyzer.

After determining the optimal frequency and pulse width range using a logic analyzer, the DRV8871 motor driver was used to run a motor. To spin the motor forward, pull the Pin 1 high and then a PWM signal inverse to the speed you want the motor to spin would be applied to PIN2. If you want the motor to spin at 25% speed forward, you would pull Pin 1 high and then apply a PWM signal with 75% duty cycle to Pin 2.

