from machine import Pin
import random
import asyncio

async def blink(led, period):
    while True:
        led.toggle()
        await asyncio.sleep(period)

loop = asyncio.get_event_loop()
loop.create_task(blink(Pin('LED', Pin.OUT), 0.25))
loop.run_forever()
