import asyncio

async def add(x, y):
    print("fast addition start")
    await asyncio.sleep(0.1)
    print("fast addition end")
    return x + y

async def mult(x, y):
    print("slow multiplication start")
    await asyncio.sleep(0.2)
    print("slow multiplication end")
    return x * y

async def main():
    task_mult = asyncio.create_task(mult(2, 6))
    task_add = asyncio.create_task(add(4, 3))
    print(await task_add, await task_mult)

asyncio.run(main())
