from time import sleep
from machine import Pin, PWM

def set_servo (angle):
    pwm.duty_u16(int((angle/180) * 6552 + 1638))
    sleep(0.01)

pwm = PWM(Pin(18))
pwm.freq(50)

while True:
    for angle in range(0, 180, 1):
        set_servo(angle)
    for angle in range(180, 0, -1):
        set_servo(angle)

