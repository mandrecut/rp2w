from machine import ADC, PWM, Pin
import time

def set_servo(angle):
    pwm.duty_u16(int((angle/180) * 6552 + 1638))
    time.sleep(0.01)

pwm = PWM(Pin(18))
pwm.freq(50)

adc=ADC(26)

while True:
    adcValue = adc.read_u16()
    angle = int((adcValue * 180) / 65535)
    set_servo(angle)
