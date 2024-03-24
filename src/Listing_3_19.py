from machine import I2S, Pin

buf = bytearray(b'some audio data ...')

audio_out = I2S(0, mode=I2S.TX, format=I2S.MONO, bits=32, rate=44100,
            sck=Pin(16), ws=Pin(17), sd=Pin(18), ibuf=40000)

audio_out.write(buf)

audio_out = I2S(0, mode=I2S.TX, format=I2S.MONO, bits=16, rate=22050,
            sck=Pin(16), ws=Pin(17), sd=Pin(18), ibuf=40000)

audio_in.readinto(buf)
