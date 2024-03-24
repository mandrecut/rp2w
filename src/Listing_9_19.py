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

import sys
import utils
import _thread

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
        q = sys.stdin.readline().strip()
        if q:
            y = json.loads(q)["d"]
            F = True
            r = [distance(y,utils.bytes2int(u[j*M:(j+1)*M])) 
                 for j in range(J//2)]
            while F:
                pass
            x = r + p
            k = (x.index(min(x))*K)//J
            print({"c":k})

u = utils.read_bytes("model.bin")
a = utils.read_json("parameters.json")
K, J, M, y, p, F = a["K"], a["J"], a["M"], [], [], False
_thread.start_new_thread(core1, ())
core0()
