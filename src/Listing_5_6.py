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

import gc
import sys
import json
import machine
import time

pwm = machine.PWM(machine.Pin(16))
adcV = machine.ADC(machine.Pin(26))
adcF = machine.ADC(machine.Pin(27))
pwm.duty_u16(32768)

gc.collect()
_N = const(1024)
_data = [0] * _N

@micropython.native
def send_data():
    t1 = time.ticks_cpu()
    for n in range(_N):
        _data[n] = adcV.read_u16()
    t2 = time.ticks_cpu()
    print(json.dumps({"data": _data,"dt": 
                       time.ticks_diff(t2, t1)}))

while True:
    q = sys.stdin.readline().strip()
    if q:
        pwm.freq(int(0.15*adcF.read_u16()+500))
        send_data()
        gc.collect()
        time.sleep(0.1)
