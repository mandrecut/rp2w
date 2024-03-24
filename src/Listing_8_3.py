from uctypes import BF_POS, BF_LEN, BFUINT32, struct
import time

GPIO0_CTRL = {
    "FUNCSEL":  0 << BF_POS | 5 << BF_LEN | BFUINT32,
    "RES1"   :  5 << BF_POS | 3 << BF_LEN | BFUINT32,
    "OUTOVER":  8 << BF_POS | 2 << BF_LEN | BFUINT32,
    "RES2"   : 10 << BF_POS | 2 << BF_LEN | BFUINT32,
    "OEOVER" : 12 << BF_POS | 2 << BF_LEN | BFUINT32,
}

GPIO0_ctrl = struct(0x40014004, GPIO0_CTRL)
GPIO0_ctrl.FUNCSEL = 0x05
GPIO0_ctrl.OEOVER  = 0x03
set_low = 0x02
set_high = 0x03

while True:
    GPIO0_ctrl.OUTOVER = set_low
    time.sleep(0.5)
    GPIO0_ctrl.OUTOVER = set_high
    time.sleep(0.5)  
