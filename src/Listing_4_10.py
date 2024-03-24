from machine import Pin, ADC, PWM
import time

adc0, adc1, adc2 = ADC(26), ADC(27), ADC(28)
pwm0, pwm1, pwm2 = PWM(Pin(16)), PWM(Pin(17)), PWM(Pin(18))
pwm0.freq(1000)
pwm1.freq(1000)
pwm2.freq(1000)

while True:
    pwm0.duty_u16(adc0.read_u16())
    pwm1.duty_u16(adc1.read_u16())
    pwm2.duty_u16(adc2.read_u16())
    time.sleep(0.1)

