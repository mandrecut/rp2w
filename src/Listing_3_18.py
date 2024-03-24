from machine import Pin, SoftI2C

i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100_000)

buf = bytearray(b'\x00\x01\x02\x03\x04\x05\x06\x07')

devices = i2c.scan()

if 0x3a in devices:
    i2c.writeto(0x3a, buf)

