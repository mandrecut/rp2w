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
import tensorflow as tf
from tensorflow import keras

def plot(fname,x,xx,xl):
    fig,n,j = plt.figure(figsize=(20, 4)),10,0
    for i in range(len(x)):
        if j == n:
            break
        if xl[i] == j:
            ax = plt.subplot(2, n, j + 1)
            plt.imshow(x[i]); plt.gray()
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            ax = plt.subplot(2, n, j + 1 + n)
            plt.imshow(xx[i]); plt.gray()
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            j += 1
    fig.savefig(fname, bbox_inches='tight')

if __name__ == "__main__":

    (x, xl),_ = keras.datasets.mnist.load_data()
    xx = tf.image.resize(np.expand_dims(x,axis=-1),[14,14])
    xx = xx[:,:,:,0]
    xx = np.sqrt(xx.numpy()).astype("int")
    plot("fig1.pdf",x,xx,xl)

    (x, xl),_ = keras.datasets.fashion_mnist.load_data()
    xx = tf.image.resize(np.expand_dims(x,axis=-1),[14,14])
    yy = yy[:,:,:,0]
    xx = np.sqrt(xx.numpy()).astype("int")
    plot("fig2.pdf",x,xx,xl)
