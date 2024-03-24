async def server():
    ip, port = connect_to_network()
    print("listening on: http://{}:{}".format(ip, port))
    asyncio.create_task(asyncio.start_server(handle_client, ip, port))
    while True:
        await asyncio.sleep(1)
