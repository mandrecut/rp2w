# Based on: https://github.com/miketeachman/micropython-i2s-examples/blob/master/examples/play_wav_from_sdcard_non_blocking.py
#           Modified by Mircea Andrecut for RP2W Pico experimenting with wav files

import os
import time
import micropython
from machine import I2S
from machine import Pin

wav_file = "music-16k-16bits-mono.wav"
wav = open(wav_file, "rb")
pos = wav.seek(44)

def i2s_callback(arg):
    n = wav.readinto(wav_samples_mv)
    if n == 0:
        audio_out.deinit()
    else:
        _ = audio_out.write(wav_samples_mv[:n])

audio_out = I2S(1, format=I2S.MONO, 
                sck=Pin(10), 
                ws=Pin(11), 
                sd=Pin(12),
                mode=I2S.TX, bits=16, 
                rate=16000, ibuf=10000)

wav_samples = bytearray(10000)
wav_samples_mv = memoryview(wav_samples)
silence = bytearray(1000)

audio_out.irq(i2s_callback)
audio_out.write(silence)

