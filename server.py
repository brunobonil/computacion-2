import datetime as dt
import time
import socket
import tqdm
import utility
import os
import multiprocessing as mp
import asyncio

def list_files():
        time.sleep(1)
        files_list = os.listdir('./shared_files_folder')
        files_list_bytes = b'|'.join([i.encode() for i in files_list])
        client.send(f'{len(files_list_bytes)}'.encode())
        time.sleep(0.01)
        client.send(files_list_bytes)

async def recv_file():
        fileInfo = client.recv(1024).decode()
        if fileInfo == '':
            return
        file, file_size = fileInfo.split('|')

        progress = tqdm.tqdm(total=int(file_size), unit="B", unit_scale=True, unit_divisor=1000)
        file_bytes = b''
        format = '.' + file.split('.')[-1]
        file_name = str(file).replace(format, '')

        while len(file_bytes) < int(file_size):
            file_bytes += client.recv(1024)
            progress.update(1024)
        print(f'Tamaño recibido: {len(file_bytes)}')
        date = dt.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')

        await asyncio.sleep(1)

        shared_file = open(f'./shared_files_folder/{file_name}-{address[0]}-{date}-{format}', 'wb')
        shared_file.write(file_bytes)
        shared_file.close()
        client.send(f'Archivo enviado exitosamente'.encode())

async def method(req_type):

        if req_type == '<GET>':
            list_files()
            
        if req_type == '<POST>':
            await asyncio.gather(recv_file(), recv_file())

        if req_type == '<DOWNLOAD>':
            send_file()

        if req_type == '<REMOVE>':
            remove_file()

def process_target(request):
    asyncio.run(method(request))

def send_file():
    file_name = client.recv(1024).decode()
    print(file_name)
    file = open(f'./shared_files_folder/{file_name}', "rb")
    file_bytes = file.read()
    print(file_bytes)
    file_to_send = (str(len(file_bytes))+'|||').encode()
    file_to_send += file_bytes
    client.sendall(file_to_send)
    file.close()

def remove_file():
        file_name = client.recv(1024).decode()
        print(file_name)
        try:
            os.remove(f'./shared_files_folder/{file_name}')
            client.send(f'File has been deleted'.encode())
        except FileNotFoundError:
            client.send(f'El archivo no existe.'.encode())



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
        print(req_type)
        p = mp.Process(target=process_target, args=(req_type,))
        p.start()
        

