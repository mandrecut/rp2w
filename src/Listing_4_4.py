import time
from machine import Pin

last_time, flag = 0, False

button = Pin(16, Pin.IN, Pin.PULL_UP)
led = Pin(15, Pin.OUT)

def button_interrupt(pin):
    global flag, last_time
    new_time = time.ticks_ms()
    if (new_time - last_time) > 300:
        led.toggle()
        last_time, flag = new_time, True

button.irq(trigger=Pin.IRQ_FALLING,
           handler=button_interrupt,
           hard=True)
while True:
    if flag == True:
        print("Interrupt!")
        flag = False

