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

import time, json
from machine import Pin, PWM
import bluetooth
from ble_advertising import advertising_payload
from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

_UART_UUID = bluetooth.UUID(UART_SERVICE_UUID)
_UART_TX = (
    bluetooth.UUID(UART_TX_CHAR_UUID),
    _FLAG_READ | _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID(UART_RX_CHAR_UUID),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
)
_UART_SERVICE = (_UART_UUID, (_UART_TX, _UART_RX),)

class BLESimplePeripheral:
    def __init__(self, ble, name="mpy-uart"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_tx, self._handle_rx),) = \
               self._ble.gatts_register_services((_UART_SERVICE,))
        self._connections = set()
        self._write_callback = None
        self._payload = advertising_payload(name=name,
                                            services=[_UART_UUID])
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("New connection", conn_handle)
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_rx and self._write_callback:
                self._write_callback(value)

    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle,
                                   self._handle_tx, data)
    def is_connected(self):
        return len(self._connections) > 0

    def _advertise(self, interval_us=500000):
        print("Starting advertising")
        self._ble.gap_advertise(interval_us,
                                adv_data=self._payload)

    def on_write(self, callback):
        self._write_callback = callback

def get_distance():
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    while not echo.value():
        pass
    tstart = time.ticks_us()
    while echo.value():
        pass
    tstop = time.ticks_us()
    distance = int(340 * time.ticks_diff(tstop, tstart) // 20000)
    return distance

def set_servo(angle):
    pwm.duty_u16(int((angle/180) * 6552 + 1638))

def on_rx(data):
    if data:
        led.on()
        a = int(data)
        set_servo(a)
        d = get_distance()
        res = json.dumps({"a":a,"d":d})
#        print(res)
        sp.send(res.encode())
        led.off()

ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble)

pwm = PWM(Pin(22))
pwm.freq(50)
led = Pin("LED", Pin.OUT)
trig = Pin(19, Pin.OUT, 0)
echo = Pin(18, Pin.IN, 0)
time.sleep(1)
set_servo(0)

while True:
    if sp.is_connected():
        sp.on_write(on_rx)