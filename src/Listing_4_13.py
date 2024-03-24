from machine import ADC, Pin, PWM
import time
import math

pwm = PWM(Pin(17))
pwm.freq(1000)
pwm.duty_u16(512)
adc = ADC(26)

in1 = Pin(15, Pin.OUT)
in2 = Pin(16, Pin.OUT)

def driveMotor(direction, speed):
    if direction:
        in1.value(1)
        in2.value(0)
    else:
        in1.value(0)
        in2.value(1)
    pwm.duty_u16(speed)

while True:
    pval = adc.read_u16()
    speed = pval - 32767
    if (pval > 32767):
        direction = 1
    else:
        direction = 0
    speed = int(math.fabs((pval-32767) * 2) - 1)
    driveMotor(direction,speed)
    time.sleep_ms(10)
