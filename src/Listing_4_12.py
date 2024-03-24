from machine import Pin
import time

def get_distance():
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    while not echo.value():
        pass
    tstart = time.ticks_us()
    while echo.value():
        pass
    tstop = time.ticks_us()
    distance = int(340 * time.ticks_diff(tstop, tstart) // 20000)
    return distance

trig = Pin(19, Pin.OUT, 0)
echo = Pin(18, Pin.IN, 0)
time.sleep(1)

while True:
    time.sleep_ms(500)
    distance = get_distance()
    print("distance = {} cm".format(distance))

