from machine import Pin, Signal
import time

led0_pin = Pin(0, Pin.OUT)
led1_pin = Pin(1, Pin.OUT)

led0_pin.value(0)
led1_pin.value(1)

print("led0=", led0_pin.value(), "led1=", led1_pin.value())
time.sleep(2)

led0 = Signal(led0_pin, invert=True)
led0.value(led0_pin.value())
led1 = Signal(led1_pin, invert=True)
led1.value(led1_pin.value())
print("led0=", led0.value(), "led1=", led1.value())

