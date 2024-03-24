import time
from machine import Pin, ADC

adc = ADC(28)
while True:
    v = (3.3/65535)*adc.read_u16()
    print("V={}V".format(V))
    time.sleep(1)

