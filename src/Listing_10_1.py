# Based on: https://github.com/micropython/micropython/blob/master/examples/bluetooth/ble_temperature.py
#           Modified for BLE reading and advertising the dht sensor values

import dht
import time
import struct
import binascii
import bluetooth
from micropython import const
from ble_advertising import advertising_payload

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_INDICATE_DONE = const(20)

_FLAG_READ = const(0x0002)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)

_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
_TEMP_CHAR = (bluetooth.UUID(0x2A6E), _FLAG_READ | _FLAG_NOTIFY | _FLAG_INDICATE,)
_HUMI_CHAR = (bluetooth.UUID(0x2A6F), _FLAG_READ | _FLAG_NOTIFY | _FLAG_INDICATE,)

_ENV_SENSE_SERVICE = (_ENV_SENSE_UUID, (_TEMP_CHAR, _HUMI_CHAR,))
_ADV_APPEARANCE_UNKNOWN = const(0)

class BLEws:

    def __init__(self, ble):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_t,self._handle_h),) = (self._ble.gatts_register_services((_ENV_SENSE_SERVICE,)))
        self._connections = set()
        address = (binascii.hexlify(self._ble.config('mac')[1],':').decode().upper())
        name = 'WS {}'.format(address)
        print('Sensor: {}'.format(name))
        self._payload = advertising_payload(name=name, services=[_ENV_SENSE_UUID], appearance=_ADV_APPEARANCE_UNKNOWN,)
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            self._advertise()
        elif event == _IRQ_GATTS_INDICATE_DONE:
            conn_handle, value_handle, status = data

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def set_data(self, temperature, humidity ,notify=False, indicate=False):

        self._ble.gatts_write(self._handle_t,temperature)
        if notify or indicate:
            for conn_handle in self._connections:
                if notify:
                    self._ble.gatts_notify(conn_handle,self._handle_t)
                if indicate:
                    self._ble.gatts_indicate(conn_handle,self._handle_t)

        self._ble.gatts_write(self._handle_h, humidity)
        if notify or indicate:
            for conn_handle in self._connections:
                if notify:
                    self._ble.gatts_notify(conn_handle,self._handle_h)
                if indicate:
                    self._ble.gatts_indicate(conn_handle,self._handle_h)

def weather_station():
    ble = bluetooth.BLE()
    ws = BLEws(ble)
    d = dht.DHT11(15)
    while True:
        f, temperature, humidity = True, 0, 0
        while f:
            time.sleep_ms(2000)
            if d.measure() == 0:
                print("DHT11 data error!")
                d = dht.DHT11(15)
            else:
                temperature = d.temperature()
                humidity = d.humidity()
                print("Temperature={:.1f}C, Humidity={:.1f}%".format(temperature, humidity));
                f = False
        temperature = str(temperature)
        humidity = str(humidity)
        ws.set_data(temperature, humidity, notify=True, indicate=False)

if __name__ == "__main__":
    weather_station()
