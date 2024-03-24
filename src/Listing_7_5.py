from machine import Pin
from rp2 import PIO, StateMachine, asm_pio

@rp2.asm_pio(out_init=(PIO.OUT_LOW,) * 5, 
                       out_shiftdir=PIO.SHIFT_RIGHT)
def sawtooth():
    set(x, 31)
    label("start")
    mov(pins,invert(x))
    jmp(x_dec,"start")
    nop()

sm = rp2.StateMachine(0, sawtooth, 
                      freq=3300000, 
                      out_base=Pin(0))
sm.active(1)
while True:
    pass
