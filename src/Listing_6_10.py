import ssl
import socket
from wifi_mode import *

with open('./cert/key.der', 'rb') as f:
    key = f.read()

with open('./cert/cert.der', 'rb') as f:
    cert = f.read()

def web_page():
    html = """<!doctype html>
    <html><head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8"/>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    </head><body>"""
    with open("toledo_javascript_chess_3.html") as f:
        html += f.read()
    html += "</body></html>"
    return html

sta_if = STA_Setup()
ip = sta_if.ifconfig()[0]
port = 8443
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, 
                         socket.SO_REUSEADDR, 1)
server_socket.bind((ip, port))
server_socket.listen(5)
print("listening on: https://{}:{}".format(ip, port))
header = "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n"

while True:
    client_socket, client_addr = server_socket.accept()
    client_socket = ssl.wrap_socket(client_socket, 
                                    server_side=True, 
                                    key=key, cert=cert)
    print("client connected from", client_addr)
    req = client_socket.readline()
    print(req)
    while True:
        r = client_socket.readline()
        if r == b"" or r == b"\r\n":
            break
        print(r)
    response = web_page()
    client_socket.write(header+response)
    client_socket.close()