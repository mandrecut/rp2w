import machine
import asyncio
from wifi_mode import *

html = "<!DOCTYPE html><html><body>"
hrml += "<h1>RP2W T=%s C</h1></body></html>"
header = "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n"

async def get_temperature():
    temperature = 437.27 - 0.0293*machine.ADC(4).read_u16()
    return str(temperature)

async def handle_client(reader, writer):
    print("Client connected")
    r = await reader.readline()
    while True:
        r = await reader.readline()
        if r == b"" or r == b"\r\n":
            break
    writer.write(header + (html % await get_temperature()))
    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")

def connect_to_network():
    sta_if = STA_Setup()
    ip = sta_if.ifconfig()[0]
    return ip, 80

async def server():
    ip, port = connect_to_network()
    print("listening on: http://{}:{}".format(ip, port))
    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(handle_client, 
                                          ip, port))
    loop.run_forever()

try:
    asyncio.run(server())
finally:
    asyncio.new_event_loop()
