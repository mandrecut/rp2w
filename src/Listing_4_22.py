# Based on: https://github.com/miketeachman/micropython-i2s-examples/blob/master/examples/record_mic_to_sdcard_blocking.py
#           Modified by Mircea Andrecut for RP2W Pico experimenting with SD card and INMP441 microphone

import os
from machine import Pin, I2S, SPI
from sdcard import SDCard

RECORD_TIME = 5
BITS_PER_SAMPLE = 32
SAMPLE_RATE = 16000
RECORDING_BYTES = RECORD_TIME*SAMPLE_RATE*BITS_PER_SAMPLE//8

def wav_header(sampleRate, bitsPerSample, record_time):
    datasize = sampleRate*record_time*bitsPerSample // 8
    o = bytes("RIFF", "ascii")
    o += (datasize + 36).to_bytes(4, "little")
    o += bytes("WAVE", "ascii")
    o += bytes("fmt ", "ascii")
    o += (16).to_bytes(4, "little")
    o += (1).to_bytes(2, "little")
    o += (1).to_bytes(2, "little")
    o += (sampleRate).to_bytes(4, "little")
    o += (sampleRate*bitsPerSample//8).to_bytes(4, "little")
    o += (bitsPerSample//8).to_bytes(2, "little")
    o += (bitsPerSample).to_bytes(2, "little")
    o += bytes("data", "ascii")
    o += (datasize).to_bytes(4, "little")
    return o

cs = Pin(13, machine.Pin.OUT)

spi = SPI(1, polarity=0, phase=0, bits=8, 
          sck=Pin(14), mosi=Pin(15), miso=Pin(12),
          firstbit=machine.SPI.MSB, 
          baudrate=1_000_000)

sd = SDCard(spi, cs)
sd.init_spi(25_000_000)
os.mount(sd, "/sd")

wav_file = "mic.wav"
wav = open("/sd/"+wav_file, "wb")

wav_header = wav_header(SAMPLE_RATE, 
                        BITS_PER_SAMPLE, 
                        RECORD_TIME)
num_bytes_written = wav.write(wav_header)

audio_in = I2S(0, format=I2S.MONO, 
               sck=Pin(16), 
               ws=Pin(17), 
               sd=Pin(18),
               mode=I2S.RX, 
               bits=32, 
               rate=SAMPLE_RATE, 
               ibuf=60000)

buf = bytearray(10000)
bufmv = memoryview(buf)
n = 0
try:
    while n < RECORDING_BYTES:
        m = audio_in.readinto(bufmv)
        if m > 0:
            nw = min(m, RECORDING_BYTES - n)
            n += wav.write(bufmv[:nw])
except (KeyboardInterrupt, Exception) as e:
    print("exception {} {}".format(type(e).__name__, e))

wav.close()
os.umount("/sd")

spi.deinit()
audio_in.deinit()

