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

import socket
import json

print("wave_type: 0-sinusoidal , 1-sawtooth, 2-triangular")
print("frequency: integer greater than 67 Hz")

while True:   
    data = input("wave_type,frequency:")
    data = data.split(",")
    data = {"w": int(data[0]),"f": 30*int(data[1])}
    data = json.dumps(data)+"\n"
    client_socket = socket.socket(socket.AF_INET, 
                                  socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.73', 8000))
    client_socket.sendall(data.encode())
    response = client_socket.recv(1024).decode()
    print(response)
    client_socket.close()
