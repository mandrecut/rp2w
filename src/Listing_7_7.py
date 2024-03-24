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

from machine import Pin
from rp2 import PIO, StateMachine, asm_pio

@asm_pio(set_init=(PIO.OUT_LOW,) * 5)
def sine():
    set(pins,0); set(pins,1); set(pins,2);
    set(pins,3); set(pins,5); set(pins,8);
    set(pins,11); set(pins,14); set(pins,17);
    set(pins,20); set(pins,23); set(pins,26);
    set(pins,28); set(pins,29); set(pins,30);
    set(pins,31); set(pins,30); set(pins,29);
    set(pins,28); set(pins,26); set(pins,23);
    set(pins,20); set(pins,17); set(pins,14);
    set(pins,11); set(pins,8); set(pins,5);
    set(pins,3); set(pins,2); set(pins,1);

@asm_pio(set_init=(PIO.OUT_LOW,) * 5)
def sawtooth():
    set(pins,1); set(pins,2); set(pins,3);
    set(pins,4); set(pins,5); set(pins,6);
    set(pins,7); set(pins,8); set(pins,9);
    set(pins,10); set(pins,11); set(pins,12);
    set(pins,13); set(pins,14); set(pins,15);
    set(pins,16); set(pins,17); set(pins,18);
    set(pins,19); set(pins,20); set(pins,21);
    set(pins,22); set(pins,23); set(pins,24);
    set(pins,25); set(pins,26); set(pins,27);
    set(pins,28); set(pins,29); set(pins,30);

@asm_pio(set_init=(PIO.OUT_LOW,) * 5)
def triangle():
    set(pins,1); set(pins,3); set(pins,5);
    set(pins,7); set(pins,9); set(pins,11);
    set(pins,13); set(pins,15); set(pins,17);
    set(pins,19); set(pins,21); set(pins,23);
    set(pins,25); set(pins,27); set(pins,29);
    set(pins,31); set(pins,29); set(pins,27);
    set(pins,25); set(pins,23); set(pins,21);
    set(pins,19); set(pins,17); set(pins,15);
    set(pins,13); set(pins,11); set(pins,9);
    set(pins,7); set(pins,5); set(pins,3);

sm = StateMachine(0, sine, freq=15000, set_base=Pin(16)) 
