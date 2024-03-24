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
import socket
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D

def animate(i):
    q = json.dumps({"send": True}) + "\n"
    y, dt = get_data(q)
    dt = dt
    fmax, dt = 500*N/dt, dt/1000
    f = np.abs(np.fft.fft(y)[0:M])
    ax[0].set_xlim(0, dt)
    ax[1].set_xlim(0, fmax)
    line.set_xdata(x*dt/N); line.set_ydata(y)
    fline.set_xdata(z*fmax/M); fline.set_ydata(f)
    ax[0].set_xticks([j for j in range(0, int(dt + 1), 2)])
    ax[1].set_xticks([j for j in range(int(fmax + 1))])
    s[0:M-1,:] = s[1:M,:]
    s[M-1,:] = np.log(f+1)
    spec = ax[2].imshow(s[::-1], cmap="hot", aspect='auto', 
                        interpolation='bicubic')
    return [line, fline, spec]

N, M = 1024, 512
[fig, ax] = plt.subplots(3, 1, layout='constrained', 
                         figsize=(14, 10.5))
x = np.arange(0, N)
line = ax[0].plot(x, [0]*N)[0]
ax[0].set_ylim(-1, 1)
ax[0].set_xlabel('Time (ms)')
ax[0].set_ylabel('Signal')
z = np.arange(0, M)
fline = ax[1].plot(z, [0]*M)[0]
ax[1].set_ylim(0, 2*np.sqrt(N))
ax[1].set_xlabel('Frequency (KHz)')
ax[1].set_ylabel('FFT PSD')
s = np.zeros((M,M))
spec = ax[2].imshow(s, 
                    cmap="hot", 
                    aspect='auto', 
                    interpolation='bicubic')
ax[2].set_axis_off()
ani = animation.FuncAnimation(fig, animate, interval=0, blit=True)
plt.show()
