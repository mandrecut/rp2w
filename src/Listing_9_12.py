async def server():
    ip, port, context = await connect_to_network()
    print("listening on: https://{}:{}".format(ip, port))
    asyncio.create_task(asyncio.start_server(handle_client, ip, port, ssl=context))
    while True:
        await asyncio.sleep(1)
