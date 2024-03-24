import socket

def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n'
                 % (path, host), 'utf8'))
    while True:
        data = s.recv(1024)
        if data:
            return str(data, 'utf8')
        else:
            break
    s.close()  
response = http_get('https://httpbin.org/get')
print(response, end='')
