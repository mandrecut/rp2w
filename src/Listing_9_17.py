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

import numpy as np
import matplotlib.pyplot as plt
import utils

def plot(fname,u,K,J):
    fig, n, j = plt.figure(figsize=(20, 20)), 10, 0
    M = J//K
    for k in range(K):
        for i in range(n):
            x = utils.bytes2int(u[(i+k*M)*98:((i+1)+k*M)*98])
            x = np.reshape(x, (14,14))
            plt.imshow(x); plt.gray()
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            j += 1
    fig.savefig(fname, bbox_inches='tight')

if __name__ == "__main__":
    u = utils.read_bytes("model.bin")
    a = utils.read_json("parameters.json")
    K, J = a["K"], a["J"]
    plot("fig_centroids.pdf", u, K, J)
