from machine import Pin, I2C

i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=100000)

devices = i2c.scan()

if 58 in devices:
    i2c.writeto(58, b'123')
    i2c.readfrom(58, 4)

