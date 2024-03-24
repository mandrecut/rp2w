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
import utils
import numpy as np
from serial import Serial
from serial.tools import list_ports

def get_serial_device(name):
    for port in list(list_ports.comports()):
        if name in port.description:
           return Serial(port.device)

q = utils.read_json("./data/test.json")
N,M = q["N"],q["M"]

y = utils.read_bytes("./data/test.bin")
yl = utils.read_bytes("./data/test_labels.bin")

y = np.array(utils.bytes2int(y))
y = np.reshape(y,(N,M*2))

pico,a = get_serial_device('Board CDC'),0

for n in range(N):
    data = json.dumps({"d":y[n].tolist()}) + "\n"
    pico.write(data.encode())
    r = pico.read_until().strip()
    d = json.loads(r.decode().replace("'",'"'))
    if d["c"] == yl[n]:
        a += 1
    print(n,":",d["c"],yl[n],round(a*100/(n+1),3),"%")
