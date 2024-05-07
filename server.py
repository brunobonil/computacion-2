import datetime as dt
import time
import socket
import tqdm
import utility
import os
import multiprocessing as mp
import asyncio

def list_files(addr, conn):
        #time.sleep(1)
        files_list = os.listdir('./shared_files_folder')
        files_list_bytes = b'|'.join([i.encode() for i in files_list])
        client.send(f'{len(files_list_bytes)}'.encode())
        time.sleep(0.01)
        client.send(files_list_bytes)
        conn.send(f'La terminal {addr} ha listado los archivos | {dt.datetime.now()}')

def recv_file(addr, conn):
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


        shared_file = open(f'./shared_files_folder/{file_name}-{address[0]}-{date}{format}', 'wb')
        shared_file.write(file_bytes)
        shared_file.close()
        client.send(f'Archivo enviado exitosamente'.encode())
        conn.send(f'La terminal {addr} ha subido un archivo | {dt.datetime.now()}')

def send_file(addr, conn):
    file_name = client.recv(1024).decode()
    file = open(f'./shared_files_folder/{file_name}', "rb")
    file_bytes = file.read()
    file_to_send = (str(len(file_bytes))+'|||').encode()
    file_to_send += file_bytes
    client.sendall(file_to_send)
    file.close()
    if client.recv(1024).decode():
        conn.send(f'La terminal {addr} ha descargado archivo(s) | {dt.datetime.now()}')

def remove_file(addr, conn):
        file_name = client.recv(1024).decode()
        print(file_name)
        try:
            os.remove(f'./shared_files_folder/{file_name}')
            client.send(f'File has been deleted'.encode())
        except FileNotFoundError:
            client.send(f'El archivo no existe.'.encode())
        conn.send(f'La terminal {addr} ha eliminado archivos | {dt.datetime.now()}')
        
def logger(conn):
    while True:    
        log = conn.recv()
        logFile = open('./server_logger.txt', 'ab')
        logFile.write(f'{log}\n{"="*100}\n'.encode())
        logFile.close()

def method(req_type, addr, conn):

        if req_type == '<GET>':
            list_files(addr, conn)
            
        if req_type == '<POST>':
            while True:
                recv_file(addr, conn)

        if req_type == '<DOWNLOAD>':
            send_file(addr, conn)

        if req_type == '<REMOVE>':
            remove_file(addr, conn)


if __name__ == '__main__':
    
    HOST = utility.get_ip()
    PORT = 9090

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    parent_conn, child_conn = mp.Pipe()
    l = mp.Process(target=logger, args=(child_conn,))
    l.start()

    while True:            
        client, address = server.accept()
        print(f'Connected to {address}')
        req_type = client.recv(1024).decode()
        p = mp.Process(target=method, args=(req_type, address[0], parent_conn))
        p.start()

