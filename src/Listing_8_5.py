from time import sleep
from dma_awg import DMAawg

dawg = DMAawg()

dawg.start(wave_type="sine", freq=10000)
sleep(5)
dawg.stop()

dawg.start(wave_type="triangle", freq=10000)
sleep(5)
dawg.stop()

dawg.start(wave_type="sawtooth", freq=10000)
sleep(5)
dawg.stop()
