from machine import Pin, SPI

spi = SPI(0, baudrate=10_000_000,
          polarity=0, phase=0, bits=8,
          sck=Pin(6), mosi=Pin(7), miso=Pin(4))

spi.write(b'12345')
spi.read(5)
buf = bytearray(5)
spi.write_readinto(b'12345', buf)
