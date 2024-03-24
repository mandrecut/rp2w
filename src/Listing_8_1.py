import time
from machine import mem32

ADDR = 0x4001_4004
OUTOVER = [0x02, 0x03]
FUNCSEL, OEOVER = 0x05, 0x03
led_off = (FUNCSEL<<0)|(OUTOVER[0]<<8)|(OEOVER<<12)
led_on = (FUNCSEL<<0)|(OUTOVER[1]<<8)|(OEOVER<<12)
print("led_off:",led_off,"led_on":led_on)

while True:
    mem32[ADDR] = led_off
    time.sleep(0.5)
    mem32[ADDR] = led_on
    time.sleep(0.5)
