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
import numpy as np
from serial import Serial
from serial.tools import list_ports
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D

def detect_rp2w(rp2w):
    for port in list_ports.comports():
        if (rp2w["name"] == port.device and
            rp2w["description"] == port.description):
            return Serial(rp2w["name"], rp2w["baudrate"])
    return None

def animate(i):
    q = json.dumps({"send": True})+"\n"
    device.write(q.encode())
    r = device.read_until().strip().decode()
    r = json.loads(r)
    dt = r["dt"]/N
    y = 3.3*np.array(r["data"])/65535
    fmax, dt = 500/dt, dt/1000
    f = np.abs(np.fft.fft(y)[0:(N//2)])/np.sqrt(N)
    ax[0].set_xlim(0, N*dt)
    ax[1].set_xlim(0, fmax)
    line.set_xdata(x*dt)
    line.set_ydata(y)

    fline.set_xdata(z*2*fmax/N)
    fline.set_ydata(f)
    ax[0].set_xticks([j for j in range(int(x[-1]*dt + 1))])
    ax[1].set_xticks([j for j in range(int(fmax + 1))])
    my = np.mean(y)
    duty0, duty1 = np.sum(y < my), np.sum(y >= my)
    duty = 100*duty1/(duty1 + duty0)
    v = np.mean([q for q in y if q > my])
    nu = 2*fmax*np.argmax(f[1:])/N
    text = ax[0].text(0.25,3.75, 
           "Vmax={:.2f}V, duty={}%, f={:.3f} KHz"
           .format(v, int(duty), nu))
    return [line, fline, text]

rp2w = {"name": "/dev/ttyACM0",
        "description": "Board in FS mode - Board CDC",
        "baudrate": 115200}

device = detect_rp2w(rp2w)
N = 1024
[fig, ax] = plt.subplots(2,1,layout='constrained',figsize=(14,7))
x = np.arange(0, N)
line = ax[0].plot(x, [0]*N)[0]
ax[0].set_ylim(0, 4)
ax[0].set_xlabel('Time (ms)')
ax[0].set_ylabel('Signal')
z = np.arange(0, N//2)
fline = ax[1].plot(z, [0]*(N//2))[0]
ax[1].set_ylim(0, np.sqrt(N))
ax[1].set_xlabel('Frequency (KHz)')
ax[1].set_ylabel('FFT PSD')
ani = animation.FuncAnimation(fig,animate,interval=0,blit=True)
plt.show()
