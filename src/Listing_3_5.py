import time
from machine import Pin

led0 = Pin(0, mode=Pin.OUT)
led1 = Pin(1, mode=Pin.OUT)
led0.off() 
led1.off()

flag = False

def led0_interrupt(pin):
    global flag
    led1.toggle()
    flag = True

led0.irq(trigger=Pin.IRQ_HIGH_LEVEL | Pin.IRQ_FALLING, 
         handler=led0_interrupt, hard=True)

while True:
    led0.toggle()
    if flag == True:
        print("Interrupt! led0={} led1={}"
               .format(led0.value(),led1.value()))
        flag = False
    time.sleep(1)


