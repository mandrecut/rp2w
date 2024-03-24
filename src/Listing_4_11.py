from machine import ADC,Pin
import time

x = ADC(28)
y = ADC(27)
z = Pin(26, Pin.IN, Pin.PULL_UP)

while True:
    print("X, Y, Z :",
           x.read_u16(),",",
           y.read_u16(), ",",
           z.value())
    time.sleep(0.1)

