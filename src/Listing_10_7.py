# Copyright (c) 2024 Mircea Andrecut
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Based on: https://github.com/micropython/micropython/blob/master/examples/bluetooth/ble_uart_peripheral.py
#           Modified for BLE radar applications

import time
import json
import asyncio
from bleak import BleakScanner, BleakClient
from bleak.backends.scanner import AdvertisementData
from bleak.backends.device import BLEDevice
import matplotlib.pyplot as plt

class BLE_UART:

    UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
    UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
    UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

    def __init__(self, peripheral_name='mpy-uart'):
        self._peripheral_name = peripheral_name
        self._rx_queue = asyncio.Queue()

    async def read(self):
        msg = await self._rx_queue.get()
        return msg

    async def write(self, msg):
        if isinstance(msg, str):
            msg = msg.encode()
        await self._client.write_gatt_char(self.UART_RX_CHAR_UUID,msg)

    async def disconnect(self):
        await self._client.disconnect()

    async def connect(self):
        self._discovery_queue = asyncio.Queue()
        device = None
        print(f"scanning for {self._peripheral_name}")
        async with BleakScanner(detection_callback=
                                self._find_uart_device):
            device: BLEDevice = await self._discovery_queue.get()
        print(f"connecting to {self._peripheral_name} ...", end="")
        client = self._client = BleakClient(device,
                                            disconnected_callback=
                                            self._handle_disconnect)
        await client.connect()
        await client.start_notify(self.UART_TX_CHAR_UUID,
                                  self._rx_handler)
        print(f" connected")

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.disconnect()

    def _rx_handler(self, _: int, data: bytearray):
        self._rx_queue.put_nowait(data)

    def _find_uart_device(self, device: BLEDevice,
                          adv: AdvertisementData):
        if device.name == self._peripheral_name:
            self._discovery_queue.put_nowait(device)

    def _handle_disconnect(self, _: BleakClient):
        self._rx_queue.put_nowait(None)

async def uart_connect():
    async with BLE_UART() as uart:
        await uart.connect()
        plt.ion()
        fig = plt.figure(figsize=(7, 7))
        ax = fig.add_subplot(polar=True)
        angles = [n*3.141593/180 for n in range(180)]
        while True:
            plt.cla()
            ax.set_thetamin(0); ax.set_thetamax(180)
            ax.set_rmin(0); ax.set_rmax(200)
            distances = [0]*180
            for angle in range(0,180,1):
                try:
                    await uart.write(str(angle).encode())
                    msg = await uart.read()
                    msg = json.loads(msg.decode())
                    print("data: ",msg)
                    if msg["d"] < 200:
                        distances[msg["a"]] = msg["d"]
                    else:
                        distances[msg["a"]] = 200
                except:
                    pass
                ax.patch.set_facecolor('0.5')
                ax.plot(angles, distances, color='black', 
                        ls='-', linewidth=0.1)
                ax.fill(angles, distances, 'w')
                fig.canvas.draw()
                fig.canvas.flush_events()
        await uart.disconnect()

if __name__ == "__main__":
    asyncio.run(uart_connect())
