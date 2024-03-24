import time
from machine import Pin

button = Pin(16, Pin.IN, Pin.PULL_DOWN)
led = Pin(15, mode=Pin.OUT)
flag = False

def button_interrupt(pin):
    global flag
    led.toggle()
    flag = True

button.irq(trigger=Pin.IRQ_FALLING, handler=button_interrupt,
           hard=True)
while True:
    if flag == True:
        print("Interrupt!")
        flag = False
