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

import gc, time, json, machine, socket
from wifi_mode import *

gc.collect()
_N = const(1024)
_data = [0]*(_N+1)
adc = machine.ADC(machine.Pin(26))
sta_if = STA_Setup()
ip = sta_if.ifconfig()[0]
port = 8000
server_socket = socket.socket()
server_socket.bind((ip, port))
server_socket.setsockopt(socket.SOL_SOCKET, 
                         socket.SO_REUSEADDR, 1)
server_socket.listen(1)
print("listening on:", (ip, port))

@micropython.native
def sample_data():
    t1 = time.ticks_us()
    for n in range(_N):
        _data[n] = adc.read_u16()
        time.sleep_us(17)
    t2 = time.ticks_us()
    _data[_N] = time.ticks_diff(t2, t1)

while True:
    try:
        client_socket, client_addr = server_socket.accept()
        q = client_socket.readline().decode()
        if len(q) > 0:
            sample_data()    
            q = ",".join([str(d) for d in _data]) + "\n"
            client_socket.sendall(q)
            gc.collect()
        else:
            print("closing")
            client_socket.close()
    except OSError as e:
        client_socket.close()
        print("client connection closed")
