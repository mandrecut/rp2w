import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.65', 8000))
client_socket.sendall("Some data".encode())
response = client_socket.recv(1024).decode()
client_socket.close()
print(response)
