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

from math import sin, pi
from array import array
from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from uctypes import BF_POS,BF_LEN,UINT32,BFUINT32,struct,addressof

class DMAawg:
    def __init__(self):
        DMA_BASE = 0x50000000
        DMA_WIDTH = 0x40
        self._nbits = 8
        self._DMA0_ADDR =  DMA_BASE
        self._DMA1_ADDR =  DMA_BASE + DMA_WIDTH
        self._PIO_BASE = 0x50200000
        self._PIO_TXF  = self._PIO_BASE + 0x010
        DMA_CHAN_CTRL = {
            "IRQ_QUIET":    21<<BF_POS | 1<<BF_LEN | BFUINT32,
            "TREQ_SEL":     15<<BF_POS | 6<<BF_LEN | BFUINT32,
            "CHAIN_TO":     11<<BF_POS | 4<<BF_LEN | BFUINT32, 
            "INCR_READ":     4<<BF_POS | 1<<BF_LEN | BFUINT32,
            "DATA_SIZE":     2<<BF_POS | 2<<BF_LEN | BFUINT32,
            "HIGH_PRIORITY": 1<<BF_POS | 1<<BF_LEN | BFUINT32,
            "EN":            0<<BF_POS | 1<<BF_LEN | BFUINT32
        }
        DMA_CHAN_REGS = {
            "READ_ADDR_REG":    0x00|UINT32,
            "WRITE_ADDR_REG":   0x04|UINT32,
            "TRANS_COUNT_REG":  0x08|UINT32,
            "CTRL_TRIG":       (0x0c,DMA_CHAN_CTRL)
        }
        DMA_ABORT = {
            "CHAN_ABORT": 0x444|UINT32
        }

        self._DMA0 = struct(self._DMA0_ADDR, DMA_CHAN_REGS)
        self._DMA1 = struct(self._DMA1_ADDR, DMA_CHAN_REGS)
        self._DMA = struct(DMA_BASE, DMA_ABORT)

    @asm_pio(out_init=(PIO.OUT_LOW,)*8,
                       out_shiftdir=PIO.SHIFT_RIGHT,
                       autopull=True)
    def _bits_output():
        out(pins, 8)

    def start(self, wave_type="sawtooth", freq=100):
        assert freq >= 8

        self._sm = StateMachine(0, self._bits_output,
                                freq=1024*freq, 
                                out_base=Pin(0))
        self._sm.active(1)

        if wave_type == "sine":
            print("sine")
            wave = array('B', [int(128+127*sin((n+0.5)*pi/128))
                               for n in range(256)])
        elif wave_type == "triangle":
            print("triangle")
            wave = array('B', [int(abs(255-2*n)) for n in range(256)])
        else:
            print("sawtooth")
            wave = array('B', [n for n in range(256)])
        pwave = array('I', [addressof(wave)])

        self._DMA0.READ_ADDR_REG = addressof(wave)
        self._DMA0.WRITE_ADDR_REG = self._PIO_TXF
        self._DMA0.TRANS_COUNT_REG = 256
        self._DMA0.CTRL_TRIG.CHAIN_TO = 1
        self._DMA0.CTRL_TRIG.INCR_READ = 1
        self._DMA0.CTRL_TRIG.IRQ_QUIET = 1
        self._DMA0.CTRL_TRIG.DATA_SIZE = 0
        self._DMA0.CTRL_TRIG.TREQ_SEL = 0x00

        self._DMA1.READ_ADDR_REG = addressof(pwave)
        self._DMA1.WRITE_ADDR_REG = self._DMA0_ADDR
        self._DMA1.TRANS_COUNT_REG = 1
        self._DMA1.CTRL_TRIG.CHAIN_TO = 0
        self._DMA1.CTRL_TRIG.IRQ_QUIET = 1
        self._DMA1.CTRL_TRIG.DATA_SIZE = 2
        self._DMA1.CTRL_TRIG.TREQ_SEL = 0x3f

        self._DMA0.CTRL_TRIG.EN = 1
        self._DMA1.CTRL_TRIG.EN = 1

    def stop(self):
        self._DMA0.CTRL_TRIG.EN = 0
        self._DMA1.CTRL_TRIG.EN = 0
        self._DMA.CHAN_ABORT = 0xFFFF
        self._sm.active(0)
