import time
import socket
import tqdm
import utility
import os

def list_files():
        files_list = os.listdir('./shared_files_folder')
        files_list_bytes = b'|'.join([i.encode() for i in files_list])
        client.send(f'{len(files_list_bytes)}'.encode())
        time.sleep(0.01)
        client.send(files_list_bytes)

def recv_file():
        file_format, file_size = client.recv(1024).decode().split('|')
        progress = tqdm.tqdm(total=int(file_size), unit="B", unit_scale=True, unit_divisor=1000)
        print(f'Tamaño real: {file_size}')
        file = b''

        while len(file) < int(file_size):
            file += client.recv(1024)
            progress.update(1024)

        print(f'Tamaño recibido: {len(file)}')

        shared_file = open(f'./shared_files_folder/{address[0]}-{time.time()}{file_format}', 'wb')
        shared_file.write(file)
        shared_file.close()
        client.send(f'File successfully sent'.encode())

def delete_file():
        file_name = client.recv(1024).decode()
        print(file_name)
        try:
            os.remove(f'./shared_files_folder/{file_name}')
            client.send(f'File has been deleted'.encode())
        except FileNotFoundError:
            client.send(f'File does not exists. Try again'.encode())

if __name__ == '__main__':
    
    HOST = utility.get_ip()
    PORT = 9090

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    while True:            
        client, address = server.accept()
        print(f'Connected to {address}')
        req_type = client.recv(1024).decode()

        if req_type == '<GET>':
            list_files()

        if req_type == '<POST>':
            recv_file()
    
        if req_type == '<REMOVE>':
             delete_file()
        



    
        
