import socket
import os
import time

HOST = '192.168.42.67'
PORT = 9090
FILE_NAME = "screenshot.png"
FORMAT = '.' + FILE_NAME.split('.')[-1]


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

file_size = os.path.getsize(FILE_NAME)

client.send(f"{FORMAT}|{str(file_size)}".encode())
#client.send(str(file_size).encode())

file = open(FILE_NAME, "rb")
data = file.read()
time.sleep(0.1)
client.sendall(data)
file.close()

client.close()