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
import json
import socket
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D
from matplotlib.widgets import Button

def increase_rate(val):
    global rate
    if rate < 480000:
        rate *= 2

def decrease_rate(val):
    global rate
    if rate > 1875:
        rate //= 2

def decrease_zoom(val):
    global zoom
    if zoom <= 0.5:
        zoom *= 2

def increase_zoom(val):
    global zoom
    if zoom >= 0.0078125:
        zoom /= 2
    print(zoom)

def recv_data(sock):
    data = ""
    while True:
        d = sock.recv(4000).decode()
        n = d.find("\n")
        if n >= 0:
            data += d[:n]
            break
        data += d
    return ''.join(data)

def get_data(q):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.66', 8000))
    q = json.dumps(q)+"\n"
    client_socket.sendall(q.encode())
    r = recv_data(client_socket)
    client_socket.close()
    r = [int(x) for x in r.split(",")]
    return 3.3*np.array(r)/4095

def animate(i):
    global rate, zoom
    q = {"samples": N, "rate": rate, "dma": 2, "adc": 0}
    dt = 1000/q["rate"]
    df = q["rate"]/N
    print(df)
    fmax = df*N/2
    y = get_data(q)
    f = np.abs(np.fft.fft(y-np.mean(y))[0:(N//2)])
    f = 0.8325*f/np.max(f)
    line.set_ydata(y)
    fline.set_ydata(f)
    ax[0].set_xlim(0, int(N*zoom+0.5))

    Vmax, Vmin = np.max(y), np.min(y)
    text1 = ax[0].text(10*zoom,3.8, 
                       "dt={:.6f}ms, Vmax={:.2f}V, Vmin={:.2f}V, 
                        SR={}, Zoom={:.2f}"
                       .format(dt, Vmax, Vmin, q["rate"], 1/zoom))

    freq = int(df*np.argmax(f))
    text2 = ax[1].text(10,.95, "df={:.2f}Hz, f={}Hz"
                                    .format(fmax/100,freq))
    return [line, fline,text1,text2]

N, zoom, rate = 2000, 1, 480000

[fig, ax] = plt.subplots(2, 1, layout='constrained', figsize=(14,7))

x = np.arange(0, N)
line = ax[0].plot(x, [0]*N)[0]
ax[0].set_ylim(0, 4)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Signal')
ax[0].set_xlim(0, N)
line.set_xdata(x)
ax[0].set_xticks([int(10*j) for j in range(N//10)])
ax[0].grid(color = 'green', linestyle = ':', linewidth = 0.25)
ax[0].set_xticklabels([])

z = np.arange(0, N//2)
fline = ax[1].plot(z, [0]*(N//2))[0]
ax[1].set_ylim(0, 1)
ax[1].set_xlabel('Frequency')
ax[1].set_ylabel('FFT PSD')
ax[1].set_xlim(0, N//2)
fline.set_xdata(z)
ax[1].set_xticks([int(10*j) for j in range(N//20)])
ax[1].grid(color = 'green', linestyle = ':', 
           linewidth = 0.25)
ax[1].set_xticklabels([])

ani = animation.FuncAnimation(fig, animate, 
                              interval=0, 
                              blit=True)

axes = plt.axes([0.75, 0.95, 0.05, 0.025])
bsrd = Button(axes, 'S-')
bsrd.on_clicked(decrease_rate)
axes = plt.axes([0.8, 0.95, 0.05, 0.025])
bsri = Button(axes, 'S+')
bsri.on_clicked(increase_rate)

axes = plt.axes([0.85, 0.95, 0.05, 0.025])
bzd = Button(axes, 'Z-')
bzd.on_clicked(decrease_zoom)
axes = plt.axes([0.9, 0.95, 0.05, 0.025])
bzi = Button(axes, 'Z+')
bzi.on_clicked(increase_zoom)
plt.show()
