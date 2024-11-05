from machine import Pin, I2C
from vl53l0x import setup_tofl_device, TBOOT
import pyb
#
device_1_xshut = Pin('D5', Pin.OUT)
device_2_xshut = Pin('D4', Pin.OUT)
device_3_xshut = Pin('D3', Pin.OUT)

i2c_1 = I2C(1)

# Set this low to disable device 1
print("Setting up device 0")
device_1_xshut.value(0)
device_2_xshut.value(0)
device_3_xshut.value(0)

pyb.delay(10)

device_1_xshut.value(1)
device_2_xshut.value(1)
device_3_xshut.value(1)

device_2_xshut.value(0)
device_3_xshut.value(0)


tofl0 = setup_tofl_device(i2c_1, 40000, 12, 8)
tofl0.set_address(0x31)

device_2_xshut.value(1)
tofl1 = setup_tofl_device(i2c_1, 40000, 12, 8)
tofl1.set_address(0x30)

device_3_xshut.value(1)
tofl2 = setup_tofl_device(i2c_1, 40000, 12, 8)
tofl2.set_address(0x29)

left, right, front = tofl0.ping(), tofl1.ping(), tofl2.ping()
print(left, 'mm, ', right, 'mm', front, 'mm') # left = tofl0.ping() # print(left, 'mm')
