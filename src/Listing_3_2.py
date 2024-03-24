from machine import Pin
import time

pins = list(range(24)) + [26,27,28]

while (True):
    for pin in pins:
        p = Pin(pin, Pin.OUT)

        p.on()
        print(p,"value:",p.value())

        time.sleep(0.1)

        p.off()
        print(p,"value:",p.value())
        time.sleep(0.1)

