from machine import UART, Pin
import time

myUART = UART(1, baudrate=9600, bits=8,
              tx=Pin(4), rx=Pin(5),
              timeout=10)
while True:
    if myUART.any() > 0:
        data = myUART.readline()
        print("data: " , data.decode('utf-8'))
