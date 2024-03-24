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
from wifi_mode import *
from sm_awg import *

sta_if = STA_Setup()
ip = sta_if.ifconfig()[0]
port = 8000
server_socket = socket.socket()
server_socket.bind((ip, port))
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.listen(1)
print("listening on:", (ip, port))
sm.active(1)

while True:
    try:
        client_socket, client_addr = server_socket.accept()
        q = client_socket.readline().decode()
        if len(q) > 0:
            q = json.loads(q)
            print(q)
            sm.active(0)
            PIO(0).remove_program(sine)
            PIO(0).remove_program(sawtooth)
            PIO(0).remove_program(triangle)
            if q["w"] == 1:
                print("sawtooth")
                sm = StateMachine(0, sawtooth, freq=q["f"], 
                                  set_base=Pin(16))
            elif q["w"] == 2:
                print("triangle")
                sm = StateMachine(0, triangle, freq=q["f"], 
                                  set_base=Pin(16))
            else:
                print("sine")
                sm = StateMachine(0, sine, freq=q["f"], 
                                  set_base=Pin(16))
            sm.active(1)
            client_socket.sendall("OK\n")
        else:
            print("closing")
            client_socket.close()
    except OSError as e:
        client_socket.close()
        print("client connection closed")
