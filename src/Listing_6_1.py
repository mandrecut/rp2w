import network
from wifi_mode import *

ap_if = AP_Setup()
print('Connected, IP address:', 
       ap_if.ifconfig()[0])
ap_if.disconnect()
