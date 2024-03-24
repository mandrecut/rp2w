import network
from secret import ssid, pswd

def STA_Setup():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ssid,pswd)
        while not sta_if.isconnected():
            pass
    return sta_if

def AP_Setup():
    local_IP = "192.168.1.10"
    gateway = "192.168.1.1"
    subnet = "255.255.255.0"
    dns = "8.8.8.8"
    ap_if = network.WLAN(network.AP_IF)
    ap_if.ifconfig([local_IP,gateway,subnet,dns])

    ap_if.config(essid=ssid, password=pswd)
    ap_if.active(True)
    while not ap_if.isconnected():
        pass
    return ap_if
