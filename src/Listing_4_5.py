from machine import Pin
import time

pir_sensor = Pin(22, Pin.IN)
previous_state = pir_sensor.value()
ti = time.time()

while True:
    current_state = pir_sensor.value()
    if current_state != previous_state:
        print("Motion detected = {}".format(time.time()-ti))
        previous_state = current_state

