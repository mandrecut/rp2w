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

import utils
import numpy as np

if __name__ == "__main__":
    q = utils.read_json("./data/test.json")
    N, M = q["N"], q["M"]

    y = utils.read_bytes("./data/test.bin")
    yl = utils.read_bytes("./data/test_labels.bin")
    y = np.array(utils.bytes2int(y))
    y = np.reshape(y,( N,M*2))

    u = utils.read_bytes("model.bin")
    p = utils.read_json("parameters.json")
    a, K, J, M = 0, p["K"], p["J"],p ["M"]

    for n in range(len(y)):
        r = [np.linalg.norm(y[n]-utils.bytes2int(u[j*M:(j+1)*M]))
             for j in range(J)]
        r = np.array(r)
        k = (K*np.argmin(r))//J
        if k == yl[n]:
            a += 1
        print(n, k, yl[n],np.round(a*100/(n+1),3),"%")
