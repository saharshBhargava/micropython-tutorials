# Driving DC Motors through DRV8871 on Arduino Giga in MicroPython

The Arduino GIGA R1 has a STM32H747XI processor. There are two advanced-control timers on the board (TIM1, TIM8) which can be used as PWM generators. They have complementary PWM outputs with programmable inserted dead times. Dead times are necessary to prevent short circuits in H-bridges motor drivers as MOSFETs are not perfect.

<img width="624" alt="Screenshot 2024-08-10 at 5 12 25 PM" src="https://github.com/user-attachments/assets/943e7c7c-85a5-4d72-8c99-a0edfaee6e4a">

One set of pins which work for motor control are the PJ6 and PJ7 pins referred to in the image above. These pins correspond to the D37 and D38 pins on the Arduino GIGA R1.
