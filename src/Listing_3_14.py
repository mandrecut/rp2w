from machine import UART, Pin
import time

UART0 = UART(0, baudrate=9600, bits=8, tx=Pin(0), rx=Pin(1), timeout=10)
UART1 = UART(1, baudrate=9600, bits=8, tx=Pin(8), rx=Pin(9), timeout=10)

while True:
    rxData = bytes()
    data = str(input("UART1: "))
    UART1.write(data)
    time.sleep(0.1)
    while UART0.any() > 0:
        rxData += UART0.read(1)
    print("UART0: " , rxData.decode('utf-8'))

