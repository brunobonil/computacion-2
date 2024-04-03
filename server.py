import time
import socket
import tqdm
import utility as u

        
HOST = u.get_ip()
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()


client, address = server.accept()
print(f'Connected to {address}')

file_format, file_size = client.recv(1024).decode('utf-8').split('|')
print(f'Tamaño real: {file_size}')
file = b''
while len(file) < int(file_size):
    file += client.recv(1024)
print(f'Tamaño recibido: {len(file)}')
shared_file = open(f'./shared_files_server/from_{address[0]}{file_format}', 'wb')
shared_file.write(file)
shared_file.close()

#progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=int(file_size))
# for i in tqdm.tqdm(range(100), total=int(file_size), unit="B", unit_scale=True, unit_divisor=1000):
#     pass
