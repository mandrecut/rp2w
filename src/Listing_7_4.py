from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
import time

@asm_pio(out_init=(PIO.OUT_HIGH,) * 8, 
         sideset_init=PIO.OUT_LOW, 
         out_shiftdir=PIO.SHIFT_RIGHT, 
         autopull=True)
def parallel():
    pull()  
    out(pins, 8).side(1)
    nop().side(0) [1]

parallel_sm = StateMachine(0, parallel, 
                           freq=2000, 
                           out_base=Pin(0), 
                           sideset_base=Pin(15))

data = [i for i in range(256)]

parallel_sm.active(1)
for i in data:
    parallel_sm.put(i)
    time.sleep(0.1)
parallel_sm.active(0)
