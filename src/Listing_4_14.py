from machine import Pin, ADC
from neopixel import NeoPixel
from time import sleep

wheel = NeoPixel(Pin(16), 8)
while True:
    adc = ADC(26).read_u16()//257
    color = [(adc, 0, 0), (0, adc, 0), (0, 0, adc)]
    for i in range(0, 8):
        wheel[i] = color[i % 3]
        wheel.write(); sleep(0.2)
        wheel[i] = (0,0,0)

