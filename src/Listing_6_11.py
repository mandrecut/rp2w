import socket
import ssl

def https_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 443)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s = ssl.wrap_socket(s)
    s.write(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n'
                   % (path, host), 'utf8'))
    while True:
        data = s.read(4096)
        if data:
            return str(data, 'utf8')
        else:
            break
    s.close()
response = https_get('https://httpbin.org/get')
print(response,end='')
