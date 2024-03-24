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
import time
import socket
import utils
from secret import ssid,pswd
import _thread

u = utils.read_bytes("model.bin")
a = utils.read_json("parameters.json")

K,J,M,y,p,F = a["K"],a["J"],a["M"],[],[],False

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, pswd)

for n in range(10):
    if wlan.status() >= 3:
        break
    print(n,'waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    ip = wlan.ifconfig()[0]
    print( 'ip = ' + ip)

addr = socket.getaddrinfo(ip,8000)[0][-1]
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(addr)
server_socket.listen(2)
print('listening on', addr)

def distance(x,y):
    return sum([(x[n]-y[n])**2 for n in range(len(x))])

def core1():
    global K,J,M,y,p,F
    while True:
        while not F:
            pass
        p = [distance(y,utils.bytes2int(u[j*M:(j+1)*M])) 
             for j in range(J//2,J)]
        F = False

def core0():
    global K,J,M,y,p,F
    while True:
        try:
            conn, addr = server_socket.accept()
            print('client connected from', addr)
            y = conn.recv(1024).decode()
            y = json.loads(y)["data"]
            F = True
            r = [distance(y,utils.bytes2int(u[j*M:(j+1)*M])) 
                 for j in range(J)]
            while F:
                pass
            r = r + p
            k = (r.index(min(r))*K)//J
            conn.sendall(json.dumps({"c":k}).encode())
            conn.close()
            gc.collect()
        except OSError as e:
            conn.close()
            print('connection closed')
 
_thread.start_new_thread(core1, ())
core0()
