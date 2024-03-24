import sys
import time
import struct
import asyncio
from bleak import BleakClient

temp_uuid = "00002a6e-0000-1000-8000-00805f9b34fb"
humi_uuid = "00002a6f-0000-1000-8000-00805f9b34fb"

async def get_ws_data(address):
    async with BleakClient(address) as client:
        if (not client.is_connected):
            raise "client not connected"
    while True:
        time.sleep(2)
        temp = await client.read_gatt_char(temp_uuid)
        humi = await client.read_gatt_char(humi_uuid)
        temp = temp.decode()
        humi = humi.decode()
        print("Temperature={}C, Humidity={}%".format(temp, humi))

if __name__ == "__main__":

    address = "28:CD:C1:0E:58:92"
    print('address:', address)
    asyncio.run(get_ws_data(address))
