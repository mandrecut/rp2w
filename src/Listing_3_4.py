from machine import Pin
import time

def get_bit(b, i):
        return (b >> i) & 1

p0 = Pin(0, Pin.OUT)
p1 = Pin(1, Pin.OUT)
p2 = Pin(2, Pin.OUT)
p3 = Pin(3, Pin.OUT)
p4 = Pin(4, Pin.OUT)
p5 = Pin(5, Pin.OUT)
p6 = Pin(6, Pin.OUT)
p7 = Pin(7, Pin.OUT)

b = 0b00000000

t0 = time.ticks_us()
while b < 256:
    p0.value(get_bit(b,0))
    p1.value(get_bit(b,1))
    p2.value(get_bit(b,2))
    p3.value(get_bit(b,3))
    p4.value(get_bit(b,4))
    p5.value(get_bit(b,5))
    p6.value(get_bit(b,6))
    p7.value(get_bit(b,7))
    print(b)
    time.sleep(0.05)
    b += 1
t1 = time.ticks_us()

print("dt={}us".format(time.ticks_diff(t1, t0)))

