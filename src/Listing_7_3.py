from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
import time

@asm_pio(out_init=(PIO.OUT_HIGH,) * 8, 
         out_shiftdir=PIO.SHIFT_RIGHT, 
         autopull=True)
def parallel():
    pull()  
    out(pins, 8)

parallel_sm = StateMachine(0, parallel, 
                           freq=125_000_000, 
                           out_base=Pin(0))

data = [i for i in range(256)]

parallel_sm.active(1)
t0 = time.ticks_us()
for i in data:
    parallel_sm.put(i)
t1 = time.ticks_us()
print("dt={}".format(time.ticks_diff(t1, t0)))
parallel_sm.active(0)
