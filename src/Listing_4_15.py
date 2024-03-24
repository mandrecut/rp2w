import dht
import machine
import time

d = dht.DHT11(machine.Pin(15))
time.sleep(1)

while True:
    time.sleep(2)
    if d.measure() == 0:
        print("DHT11 data error!")
        d = dht.DHT11(machine.Pin(15))
        time.sleep(1)
    else:
        t = d.temperature()
        h = d.humidity()
        print("temperature: {:.2f}C, humidity: {:.2f}".format(t, h))