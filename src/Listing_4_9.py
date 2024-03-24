from machine import Pin,PWM
import math
import time

button = Pin(16, Pin.IN, Pin.PULL_UP)
buzz = PWM(Pin(15)); buzz.freq(1000)

def alert():
    for x in range(0, 36):
        s  = math.sin(x * 10 * 3.141593 / 180)
        t = 1500+int(s*500)
        buzz.freq(t)
        time.sleep_ms(10)

try:
    while True:
        if not button.value():
            buzz.duty_u16(4092*2)
            alert()
        else:
            buzz.duty_u16(0)
except:
    buzz.deinit()


