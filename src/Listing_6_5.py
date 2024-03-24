import network

wlan=network.WLAN(network.STA_IF)
wlan.active(True)
access_points = wlan.scan()

for ap in access_points:
    print(ap)
