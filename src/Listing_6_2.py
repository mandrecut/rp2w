from wifi_mode import *

sta_if = STA_Setup()
print('Connected, IP address:', 
       sta_if.ifconfig()[0])
sta_if.disconnect()
