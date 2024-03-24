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

def write_json(filename,data):
    f = open(filename, 'w')
    print(json.dumps(data,separators=(",",":")), file=f)
    f.close()

def read_json(fname):
    f = open(fname, 'r')
    data = json.load(f)
    f.close()
    return data

def write_bytes(filename,data):
    f = open(filename, 'wb')
    f.write(data)
    f.close()

def read_bytes(filename):
    f = open(filename, 'rb')
    data = f.read()
    f.close()
    return data

def bytes2int(b):
    z = []
    for x in b:
        z.append((x&(0xF0))>>4)
        z.append(x&(0x0F))
    return z
