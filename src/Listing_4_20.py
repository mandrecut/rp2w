# Based on: https://github.com/miketeachman/micropython-i2s-examples/blob/master/examples/play_tone.py
#           Modified by Mircea Andrecut for RP2W Pico interfacing with PCM5102

import math
import struct
from machine import Pin, I2S

TONE_FREQ = 1000
VOLUME_REDUCTION = 4
SAMPLE_RATE = 8000
BYTES_PER_SAMPLE = 2

audio_out = I2S(1, sck=Pin(10), ws=Pin(11), sd=Pin(12),
                mode=I2S.TX, bits=8*BYTES_PER_SAMPLE,
                format=I2S.MONO, rate=SAMPLE_RATE, ibuf=10000)

N_SAMPLES = SAMPLE_RATE//TONE_FREQ
BUF_SIZE = N_SAMPLES * BYTES_PER_SAMPLE
buf = bytearray(BUF_SIZE)

for i in range(N_SAMPLES):
    a = pow(2, 8*BYTES_PER_SAMPLE-1)//VOLUME_REDUCTION
    s = a + int((a-1)*math.sin(2*math.pi*i/N_SAMPLES))
    struct.pack_into("<h", buf, i*BYTES_PER_SAMPLE, s)

try:
    while True:
        n = audio_out.write(buf)
except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))

audio_out.deinit()
