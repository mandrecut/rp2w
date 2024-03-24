from machine import Pin
import time

button = Pin(16, Pin.IN, Pin.PULL_UP)
led = Pin(15, Pin.OUT)
while True:
    if not button.value():
        time.sleep(0.1)
        if button.value():
            led.toggle()

