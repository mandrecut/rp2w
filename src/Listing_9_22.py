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
import time
import numpy as np
import socket
import utils

q = utils.read_json("./data/test.json")
N,M = q["N"],q["M"]
y = utils.read_bytes("./data/test.bin")
yl = utils.read_bytes("./data/test_labels.bin")

a = 0
for n in range(N):
    x = {"data":utils.bytes2int(y[n*98:(n+1)*98])}
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.66',8000))
    client_socket.sendall(json.dumps(x).encode())
    data = client_socket.recv(64).decode()
    k = json.loads(data)["c"]
    if k == yl[n]:
        a += 1
    print(n,":",k,yl[n],round(a*100/(n+1),3),"%")
    client_socket.close()
