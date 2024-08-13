import pyb
from pyb import Pin, Timer, I2C

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
        self.direction=direction ## todo complete, if required

class DualPWM:
    def __init__(self, pin_number, pin_number_n, alt_function, timer, channel_number):
        self.pin = Pin(pin_number, mode=Pin.OUT_PP,value=1)
        self.pin_n = Pin(pin_number_n, mode=Pin.OUT_PP,value=1)
        self.alt_function=alt_function
        self.timer = timer
        self.channel_number=channel_number
        self.channel = self.timer.channel(channel_number, Timer.PWM,  pulse_width_percent=0)
        
    def pulse_width_percent(self, percentage):
        if percentage > 100:
            percentage = 100
        if percentage < 0:
            percentage =0
        pw = int(24000*percentage/100)
        self.channel.pulse_width(pw) # max 24k
        #print("stting pw to:",pw)

    def stop(self):
        self.timer.deinit() 

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
        
     
timer = pyb.Timer(8, freq=10000, deadtime=1008)

#Right Motor
pwm_right = DualPWM('PJ7','PJ6',alt_function=pyb.Pin.AF3_TIM8,timer=timer,channel_number=2)
motor_right = Motor(1, pwm_right)


#Left Motor
pwm_left = DualPWM( 'PH15','PK0',alt_function=pyb.Pin.AF3_TIM8,timer=timer,channel_number=3)
motor_left = Motor(0, pwm_left)

print("moving forward..")
motor_left.set_direction(0)
motor_right.set_direction(1)
motor_left.set_speed_percentage(50)
motor_right.set_speed_percentage(50)
pyb.delay(2000)

motor_left.set_speed_percentage(0)
motor_right.set_speed_percentage(0)
pyb.delay(1000)

print("moving backward..")
motor_left.set_direction(1)
motor_right.set_direction(0)
motor_left.set_speed_percentage(50)
motor_right.set_speed_percentage(50)

pyb.delay(2000)

motor_left.set_speed_percentage(0)
motor_right.set_speed_percentage(0)


