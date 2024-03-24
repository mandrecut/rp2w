import socket
from wifi_mode import *

sta_if = STA_Setup()
ip = sta_if.ifconfig()[0]
port = 8000
server_socket = socket.socket()
server_socket.bind((ip, port))
server_socket.setsockopt(socket.SOL_SOCKET, 
                         socket.SO_REUSEADDR, 1)
server_socket.listen(1)
print("listening on:", (ip, port))

while True:
    try:
        client_socket, client_addr = server_socket.accept()
        print("client connected from", client_addr)
        data = client_socket.recv(1024).decode()
        print(data)
        if len(data) > 0:
            client_socket.send(b"Got it, thanks!")
        else:
            client_socket.close()
    except OSError as e:
        client_socket.close()
        print("client connection closed")
