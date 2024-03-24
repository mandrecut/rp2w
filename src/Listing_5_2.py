import json
from serial import Serial
from serial.tools import list_ports

def detect_rp2w(rp2w):
    for port in list_ports.comports():
        if (rp2w["name"] == port.device and 
            rp2w["description"] == port.description):
            return Serial(rp2w["name"], rp2w["baudrate"])
    return None

rp2w = {"name": "/dev/ttyACM0",
        "description": "Board in FS mode - Board CDC",
        "baudrate": 115200}

device = detect_rp2w(rp2w)

if device:
    print(device)
    json_message = {"host": "Hello device!"}
    string_message = json.dumps(json_message) + "\n"
    device.write(string_message.encode())
    response = device.read_until().strip()
    response = json.dumps(response.decode())
    print(response)
    device.close()
