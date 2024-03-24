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

def recv_data(sock):
    data = ""
    while True:
        d = sock.recv(4096).decode()
        n = d.find("\n")
        if n >= 0:
            data += d[:n]
            break
        data += d
    return data.split(",")
    
def get_data(q):
    client_socket = socket.socket(socket.AF_INET, 
                                  socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.65', 8000))
    client_socket.sendall(q.encode())
    r = recv_data(client_socket)
    r, dt = [int(x) for x in r[:-1]], int(r[-1])
    return np.array(r)/32768-1, dt

def animate(i):
    q = json.dumps({"send": True}) + "\n"
    y, dt = get_data(q)
    fmax, dt = 500*N/dt, dt/1000
    f = np.abs(np.fft.fft(y)[0:(N//2)])
    ax[0].set_xlim(0, dt)
    ax[1].set_xlim(0, fmax)
    line.set_xdata(x*dt/N) 
    line.set_ydata(y)
    fline.set_xdata(z*2*fmax/N) 
    fline.set_ydata(f)
    ax[0].set_xticks([j for j in range(0, int(dt + 1), 2)])
    ax[1].set_xticks([j for j in range(int(fmax + 1))])
    return [line, fline]
N = 1024
[fig, ax] = plt.subplots(2, 1, layout='constrained', 
                         figsize=(14, 7))
x = np.arange(0, N)

line = ax[0].plot(x, [0]*N)[0]
ax[0].set_ylim(-1, 1)
ax[0].set_xlabel('Time (ms)')
ax[0].set_ylabel('Signal')
z = np.arange(0, N//2)
fline = ax[1].plot(z, [0]*(N//2))[0]
ax[1].set_ylim(0, 2*np.sqrt(N))
ax[1].set_xlabel('Frequency (KHz)')
ax[1].set_ylabel('FFT PSD')
ani = animation.FuncAnimation(fig, animate, 
                              interval=0, blit=True)
plt.show()
