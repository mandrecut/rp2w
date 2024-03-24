import machine
import time
import rp2

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    set(pins, 1) [24]
    nop()        [24]
    nop()        [24]
    nop()        [24]
    nop()        [24]
    set(pins, 0) [24]
    nop()        [24]
    nop()        [24]
    nop()        [24]
    nop()        [24]
    wrap()

sm = rp2.StateMachine(0)
sm.init(blink, freq=2500, set_base=machine.Pin(15))
sm.active(1)
time.sleep(3)
sm.active(0)
