import time
from machine import Pin
import rp2

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink_1hz():
    irq(rel(0))
    set(pins, 1)
    set(x, 31)                  [5]   
    label("delay_high")
    nop()                       [29]
    jmp(x_dec, "delay_high")
    set(pins, 0)
    set(x, 31)                  [6]
    label("delay_low")
    nop()                       [29]
    jmp(x_dec, "delay_low")

sm = rp2.StateMachine(0, blink_1hz, freq=2000, 
                      set_base=Pin(15))
sm.irq(lambda p: print(time.ticks_ms()))

sm.active(1)
time.sleep(10)
sm.active(0)
