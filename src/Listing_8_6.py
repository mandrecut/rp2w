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
#
# Inspired by: https://github.com/jbentham/pico/blob/main/rp_devices.py
#              Copyright (c) 2021 Jeremy P Bentham
#              Modified by Mircea Andrecut as a class restricted to ADC

import array
from machine import ADC
from uctypes import addressof
from uctypes import BF_POS, BF_LEN, UINT32, BFUINT32, struct
import gc

class DMAadc(ADC):
    def __init__(self, adc_chan=0, dma_chan=0, samples=2000):
        super().__init__(26+adc_chan)
        assert adc_chan >= 0 and adc_chan <= 2
        assert dma_chan >= 0 and dma_chan <= 11
        assert samples >= 16 and samples <= 3000
        self._samples = samples
        gc.collect()
        self._buf = array.array('H', [0]*self._samples)
        DMA_BASE  = 0x50000000
        DMA_WIDTH = 0x40
        DMA_COUNT = 12
        ADC_BASE  = 0x4004c000
        ADC_FIFO  = 0x4004c00c
        DREQ_ADC  = 36

        DMA_CTRL = {
            "BUSY":       24<<BF_POS | 1<<BF_LEN | BFUINT32,
            "IRQ_QUIET":  21<<BF_POS | 1<<BF_LEN | BFUINT32,
            "TREQ_SEL":   15<<BF_POS | 6<<BF_LEN | BFUINT32,
            "CHAIN_TO":   11<<BF_POS | 4<<BF_LEN | BFUINT32,
            "INCR_WRITE":  5<<BF_POS | 1<<BF_LEN | BFUINT32,
            "DATA_SIZE":   2<<BF_POS | 2<<BF_LEN | BFUINT32,
            "EN":          0<<BF_POS | 1<<BF_LEN | BFUINT32
        }
        DMA_REGS = {
            "READ_ADDR_REG":    0x00|UINT32,
            "WRITE_ADDR_REG":   0x04|UINT32,
            "TRANS_COUNT_REG":  0x08|UINT32,
            "CTRL_TRIG":       (0x0c,DMA_CTRL)
        }
        DMA_ABORT = {
            "CHAN_ABORT": 0x444|UINT32
        }
        ADC_CS = {
            "AINSEL":     12<<BF_POS | 3<<BF_LEN | BFUINT32,
            "READY":       8<<BF_POS | 1<<BF_LEN | BFUINT32,
            "START_MANY":  3<<BF_POS | 1<<BF_LEN | BFUINT32,
            "EN":          0<<BF_POS | 1<<BF_LEN | BFUINT32
        }

        ADC_FCS = {
            "THRESH":  24<<BF_POS | 4<<BF_LEN | BFUINT32,
            "OVER":    11<<BF_POS | 1<<BF_LEN | BFUINT32,
            "UNDER":   10<<BF_POS | 1<<BF_LEN | BFUINT32,
            "EMPTY":    8<<BF_POS | 1<<BF_LEN | BFUINT32,
            "DREQ_EN":  3<<BF_POS | 1<<BF_LEN | BFUINT32,
            "EN":       0<<BF_POS | 1<<BF_LEN | BFUINT32,
        }
        ADC_REGS = {
            "CS":   (0x00,ADC_CS),
            "FCS":  (0x08,ADC_FCS),
            "FIFO":  0x0c|UINT32,
            "DIV":   0x10|UINT32,
        }

        self._DMA_CHAN = struct(DMA_BASE + dma_chan*DMA_WIDTH, DMA_REGS)
        self._DMA = struct(DMA_BASE, DMA_ABORT)
        self._ADC_CHAN = struct(ADC_BASE, ADC_REGS)

        self._adc_chan = adc_chan
        self._ADC_CHAN.CS.EN = 1
        self._ADC_CHAN.FCS.EN = 1
        self._ADC_CHAN.FCS.DREQ_EN = 1
        self._ADC_CHAN.FCS.THRESH = 1
        self._ADC_CHAN.FCS.OVER = 1
        self._ADC_CHAN.FCS.UNDER = 1
        self._ADC_CHAN.CS.AINSEL = self._adc_chan

        self._dma = DMA_BASE
        self._DMA_CHAN.READ_ADDR_REG = ADC_FIFO
        self._DMA_CHAN.CTRL_TRIG.CHAIN_TO = dma_chan
        self._DMA_CHAN.CTRL_TRIG.INCR_WRITE = 1
        self._DMA_CHAN.CTRL_TRIG.IRQ_QUIET = 1
        self._DMA_CHAN.CTRL_TRIG.DATA_SIZE = 1
        self._DMA_CHAN.CTRL_TRIG.TREQ_SEL = DREQ_ADC

    def capture(self, rate=120000):
        assert rate >= 1000
        self._clear_fifo()
        self._ADC_CHAN.CS.AINSEL = self._adc_chan
        self._DMA_CHAN.WRITE_ADDR_REG = addressof(self._buf)
        self._DMA_CHAN.TRANS_COUNT_REG = self._samples
        self._ADC_CHAN.DIV = (48000000//rate - 1) << 8
        self._DMA_CHAN.CTRL_TRIG.EN = 1
        self._ADC_CHAN.CS.START_MANY = 1
        while self._DMA_CHAN.CTRL_TRIG.BUSY:
            pass
        self._ADC_CHAN.CS.START_MANY = 0
        self._DMA_CHAN.CTRL_TRIG.EN = 0
        return self._buf

    def _clear_fifo(self):
        while not self._ADC_CHAN.CS.READY:
            pass
        while not self._ADC_CHAN.FCS.EMPTY:
            _ = self._ADC_CHAN.FIFO

    def stop(self):
        self._DMA.CHAN_ABORT = 0xFFFF
