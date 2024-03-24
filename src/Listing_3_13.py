from machine import Pin, Timer
from time import sleep

led0 = machine.Pin(0, Pin.OUT)
led1 = machine.Pin(1, Pin.OUT)

led0Timer = Timer()
led1Timer = Timer()

def toggle_led0(timer):
    led0.toggle()

def toggle_led1(timer):
    led1.toggle()

led0Timer.init(period=1000, mode=Timer.PERIODIC, callback=toggle_led0)

led1Timer.init(freq=2, mode=Timer.PERIODIC, callback=toggle_led1)

