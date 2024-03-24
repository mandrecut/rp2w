from machine import Pin
import time

# create an input on pin 0, with a pull up resistor
p = Pin(0, Pin.IN, Pin.PULL_UP)
time.sleep(0.1)
print(p.value())

# reconfigure the pin 0 with a pull down resistor
p.init(p.IN, p.PULL_DOWN)
time.sleep(0.1)
print(p.value()

