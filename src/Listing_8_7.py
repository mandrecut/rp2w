import time
import machine
from dma_adc import DMAadc

pwm = machine.PWM(machine.Pin(16))
pwm.freq(48000)
pwm.duty_u16(32768)

dma_adc = DMAadc(adc_chan=0, dma_chan=2, samples=2000)
while True:
    data = dma_adc.capture(rate=480000)
    for d in data:
        print(d)
    time.sleep(1)
