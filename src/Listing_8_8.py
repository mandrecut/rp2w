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

import json
import socket
from machine import PWM, Pin
from dma_adc import DMAadc
from wifi_mode import *
import gc

pwm = PWM(Pin(16))
pwm.freq(10000)
pwm.duty_u16(32768)

sta_if = STA_Setup()
ip = sta_if.ifconfig()[0]
port = 8000
server_socket = socket.socket()
server_socket.bind((ip, port))
server_socket.setsockopt(socket.SOL_SOCKET, 
                         socket.SO_REUSEADDR, 1)
server_socket.listen(1)
print("listening on:", (ip, port))
while True:
    try:
        client_socket, client_addr = server_socket.accept()
        q = client_socket.readline().decode()
        if len(q) > 0:
            q = json.loads(q)
            dma_adc = DMAadc(adc_chan=q["adc"], 
                             dma_chan=q["dma"], 
                             samples=q["samples"])
            data = dma_adc.capture(rate=q["rate"])
            dma_adc.stop()
            client_socket.sendall(",".join([str(d) 
                                  for d in data])+"\n")
            data = None
            gc.collect()
        else:
            print("closing")
            client_socket.close()
    except OSError as e:
        client_socket.close()
        print("client connection closed")
