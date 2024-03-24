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
from tensorflow import keras
import tensorflow as tf
import utils

if __name__ == "__main__":
    (x, xl),(y,yl) = keras.datasets.mnist.load_data()
#    (x, xl),(y,yl) = keras.datasets.fashion_mnist.load_data()
    x = tf.image.resize(np.expand_dims(x,axis=-1),[14,14])
    y = tf.image.resize(np.expand_dims(y,axis=-1),[14,14])

    x = x[:,:,:,0].numpy()
    y = y[:,:,:,0].numpy()
    x = np.sqrt(x.numpy()).astype("int")
    y = np.sqrt(y.numpy()).astype("int")
    (N,L,L) = np.shape(x)
    x = np.reshape(x,(N,L*L))
    (N,M) = np.shape(x)
    x = [(x[n,m]<<4)|x[n,m+1] for n in range(N) for m in range(0,M,2)]
    x = bytearray(x)    
    utils.write_bytes("./data/train.bin",x)
    utils.write_bytes("./data/train_labels.bin",xl)
    utils.write_json("./data/train.json",{"N":N,"M":M//2})
    (N,L,L) = np.shape(y)
    y = np.reshape(y,(N,L*L))
    (N,M) = np.shape(y)
    y = [(y[n,m]<<4)|y[n,m+1] for n in range(N) for m in range(0,M,2)]
    y = bytearray(y)
    utils.write_bytes("./data/test.bin",y)
    utils.write_bytes("./data/test_labels.bin",yl)
    utils.write_json("./data/test.json",{"N":N,"M":M//2})
