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
from sklearn.cluster import KMeans

def kmeans(J,K,x,xl):
    (N,L) = np.shape(x)
    u = np.zeros((K*J,L), dtype="float32")
    for k in range(K):
        kmeans = KMeans(n_clusters=J, 
                        n_init='auto', 
                        random_state=123)
        kmeans.fit(x[xl==k])
        u[k*J:(k+1)*J] = kmeans.cluster_centers_
        print("k=",k)
    return u.astype("int")

if __name__ == "__main__":
    J = 16
    q = utils.read_json("./data/train.json")
    N, M = q["N"], q["M"]

    x = utils.read_bytes("./data/train.bin")
    xl = utils.read_bytes("./data/train_labels.bin")

    x = np.array(utils.bytes2int(x))
    x = np.reshape(x, (N, M*2))

    xl = np.array([int(n) for n in xl])
    K = np.max(xl)+1

    u = kmeans(J, K, x, xl)
    (J,M) = np.shape(u)
    u = [(u[j,m]<<4)|u[j,m+1] for j in range(J) for m in range(0,M,2)]
    u = bytearray(u)

    utils.write_bytes("model.bin",u)
    utils.write_json("parameters.json", {"K": int(K), "J": int(J), "M": int(M)//2})
