from machine import Pin
import time

button = Pin(16, Pin.IN, Pin.PULL_UP)
led = Pin(15, Pin.OUT)
last_time = 0 
while True:
    if not button.value():
        new_time = time.ticks_ms()
        if (new_time - last_time) > 300:
            led.toggle()
            last_time = new_time

