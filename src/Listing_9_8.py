import asyncio
import random

async def add(x):
    return sum(x)

async def get_results_coros(data):
    coros = [add(x) for x in data]
    results = await asyncio.gather(*coros)
    return results

async def get_results_tasks(data):
    tasks = [asyncio.create_task(add(x)) for x in data]
    results = await asyncio.gather(*tasks)
    return results

data = [[random.random() for i in range(5)] for j in range(4)]
print("data=", data)

results_coros = asyncio.run(get_results_coros(data))
print("results_coros=", results_coros)
print("total_coros=", sum(results_coros))

results_tasks = asyncio.run(get_results_tasks(data))
print("results_tasks=", results_coros)
