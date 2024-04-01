import socket
import os
import time


HOST = '192.168.100.156'
PORT = 9090

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

file_size = os.path.getsize("dog.jpg")

client.send("recv_image.jpg|".encode())
client.send(str(file_size).encode())

file = open("dog.jpg", "rb")
data = file.read()
time.sleep(0.1)
client.sendall(data)
client.send(b"<FILE FULLY SENT>")
file.close()

client.close()