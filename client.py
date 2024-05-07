import socket
import os
import time
import argparse
import utility
import tqdm
import asyncio


HOST = utility.get_ip()
PORT = 9090
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def listar():
    client.send(f'<GET>'.encode())
    msg_len = client.recv(1024).decode()
    files_list = client.recv(int(msg_len)).decode().split('|')
    print('LISTA DE ARCHIVOS')
    [print(f'>>> {i}') for i in files_list]

async def enviar(file_name):
    file_list = args.file
    #for file_name in file_list:
    file_size = os.path.getsize(file_name)
    client.send(f"{file_name}|{str(file_size)}".encode())

    file = open(file_name, "rb")
    data = file.read()
    time.sleep(0.01)
    client.sendall(data)
    file.close()
    print(client.recv(1024).decode())

async def enviar_concurrente(file_list):
    tasks = [enviar(file) for file in file_list]
    await asyncio.gather(*tasks)


def descargar():
    client.send(f'<DOWNLOAD>'.encode())
    time.sleep(0.01)
    file_name = args.download
    client.send(file_name.encode())
    file_size, file = client.recv(1024).split(b'|||')
    progress = tqdm.tqdm(total=int(file_size), unit="B", unit_scale=True, unit_divisor=1000)

    while len(file) < int(file_size):
        file += client.recv(1024)
        progress.update(1024)
    client.send('<DONE>'.encode())
    
    new_file = open(f'./client_folder/{file_name}', 'wb')
    new_file.write(file)
    new_file.close()

def borrar():
    client.send(f'<REMOVE>'.encode())
    time.sleep(0.01)
    file = args.remove
    client.send(file.encode())
    print(client.recv(1024).decode())
    client.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser("Terminal del cliente")
    parser.add_argument('-f', '--file', type=str, nargs='+', help='Especifica la ruta o archivos que se va a enviar')
    parser.add_argument('-l', '--list', action='store_true', help='Devuelve un listado de los archivos en el servidor')
    parser.add_argument('-d', '--download', type=str, help='Descarga el archivo especificado')
    parser.add_argument('-r', '--remove', type=str, help='Elimina el archivo especificado en el servidor remoto')
    args = parser.parse_args()

    if args.list:
        listar()

    if args.file:
        client.send(f'<POST>'.encode())
        time.sleep(0.01)
        asyncio.run(enviar_concurrente(args.file))

    if args.download:
        descargar()

    if args.remove:
        borrar()
