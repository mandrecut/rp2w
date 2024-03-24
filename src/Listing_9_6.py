from machine import Pin
import random
import asyncio

async def blink(led, period):
    while True:
        led.toggle()
        await asyncio.sleep(period)

async def main():
    pins = list(range(24)) + [26,27,28]
    for n in pins:
        asyncio.create_task(blink(Pin(n, Pin.OUT), 
                            random.random()))
    await asyncio.sleep(60)

asyncio.run(main())
