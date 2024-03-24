from machine import Pin, ADC
import time
import math

adc=ADC(26)

while True:
    adcV = adc.read_u16()
    V = 3.3 * adcV / 65535
    RT = 10 * V / (3.3 - V)
    TK = (1 / (1 / (273.15 + 25) + (math.log(RT/10)) / 3950))
    TC = int(TK - 273.15)
    print("ADC={}, V={}, T={}C".format(adcV, V,TC))
    time.sleep(1)

