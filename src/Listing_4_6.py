from machine import Pin
import time

pir_sensor = Pin(22, Pin.IN)
current_state = 0
previous_state = 0
ti = time.time()

def pir_interrupt(Pin):
    global current_state
    current_state = (current_state + 1) % 2

pir_sensor.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, 
               handler=pir_interrupt)
while True:
    if current_state != previous_state:
        print("Motion detected {}".format(time.time()-ti))
        previous_state = current_state

