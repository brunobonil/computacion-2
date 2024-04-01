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

file_name, file_size = client.recv(1024).decode('utf-8').split('|')
print(file_name)
print(file_size)
file = client.recv(int(file_size))
print(file)

#file = open(file_name, 'wb')
#file_bytes = b""

done = False

#progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=int(file_size))


