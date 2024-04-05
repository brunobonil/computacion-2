import socket
import os
import time
import argparse
import utility

parser = argparse.ArgumentParser("Terminal del cliente")
parser.add_argument('-f', '--file', help='Especifica la ruta o archivos que se va a enviar')
parser.add_argument('-l', '--list', action='store_true', help='Devuelve un listado de los archivos en el servidor')
parser.add_argument('-c', '--close', action='store_true', help='Cierra la conexion con el servidor')
args = parser.parse_args()

HOST = utility.get_ip()
PORT = 9090
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

if args.list:
    client.send(f'<GET>'.encode())
    msg_len = client.recv(1024).decode()
    files_list = client.recv(int(msg_len)).decode().split('|')
    print('LISTA DE ARCHIVOS')
    [print(f'>>>{i}') for i in files_list]


if args.file:
    client.send(f'<POST>'.encode())
    time.sleep(0.01)
    FILE_NAME = args.file
    FORMAT = '.' + FILE_NAME.split('.')[-1]
    # Agregar el nombre original del archivo, junto con el formato
    file_size = os.path.getsize(FILE_NAME)
    client.send(f"{FORMAT}|{str(file_size)}".encode())

    file = open(FILE_NAME, "rb")
    data = file.read()
    time.sleep(0.1)
    client.sendall(data)
    file.close()

    client.close()