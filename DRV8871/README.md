# Driving DC Motors through DRV8871 on Arduino Giga in MicroPython

The Arduino GIGA R1 has a STM32H747XI processor. There are two advanced-control timers on the board (TIM1, TIM8) which can be used as PWM generators. They have complementary PWM outputs with programmable inserted dead times. Dead times are necessary to prevent short circuits in H-bridges motor drivers as MOSFETs are not perfect.


