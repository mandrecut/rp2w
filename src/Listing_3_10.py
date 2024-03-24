from machine import Pin, PWM

pwm0 = PWM(Pin(0))
duty0 = int(0.33*65535)
pwm0.freq(1000)
pwm0.duty_u16(duty0)

pwm2 = PWM(Pin(2))
duty2 = int(0.66*65535)
pwm2.freq(1000)
pwm2.duty_u16(duty2)

while True:
    pass

