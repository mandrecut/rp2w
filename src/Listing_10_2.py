import asyncio
from bleak import BleakClient

async def scan(address):
  async with BleakClient(address) as client:
    if (not client.is_connected):
        raise "client not connected"
    for service in client.services:
        print("[Service]", service)
        for char in service.characteristics:
            if "read" in char.properties:
                try:
                    val=await client.read_gatt_char(char.uuid)
                    print(" [Characteristic] {} ({}), Value:{}".format(char,",".join(char.properties),val))
                except Exception as e:
                    print(" [Characteristic] {} ({}), Error:{}".format(char,",".join(char.properties),e))
            else:
                print(" [Characteristic] {} ({})".format(char, ",".join(char.properties)))
            for descriptor in char.descriptors:
                try:
                    val = await client.read_gatt_descriptor(descriptor.handle)
                    print("  [Descriptor] {}, Value: {}".format(descriptor,val))
                except Exception as e:
                    print("  [Descriptor] {}, Value: {}".format(descriptor, e))

if __name__ == "__main__":
    address = "28:CD:C1:0E:58:92"
    print('address:', address)
    asyncio.run(scan(address))
