import socket

HOST = '192.168.1.45'
PORT = 9090

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.send(f"Hello I'm a client".encode('utf-8'))
while True:
    print(client.recv(1024).decode('utf8'))
    client.send(input("Mensaje para el servidor: ").encode('utf-8'))