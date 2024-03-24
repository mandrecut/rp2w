from machine import Pin, PWM
from time import sleep

pwm0 = PWM(Pin(0))
pwm1 = PWM(Pin(1))
pwm0.freq(1000)
pwm1.freq(1000)

while True:
    for duty in range(65535):
        pwm0.duty_u16(duty)
        pwm1.duty_u16(65535-duty)
    for duty in range(65535, 0, -1):
        pwm0.duty_u16(duty)
        pwm1.duty_u16(65535-duty)

