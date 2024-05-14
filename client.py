import socket
import os
import time
import argparse
import utility
import tqdm


HOST = utility.get_ip()
PORT = 9090
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def listar():
    client.send(f'<GET>'.encode())
    print(client.recv(1024).decode()) # Recibe mensaje del servidor indicando si tiene permisos o no
    msg_len = client.recv(1024).decode()
    files_list = client.recv(int(msg_len)).decode().split('|')
    print('LISTA DE ARCHIVOS')
    [print(f'>>> {i}') for i in files_list]

def enviar():
    file_list = args.file
    for file_name in file_list:
        file_size = os.path.getsize(file_name)
        client.send(f"{file_name}|{str(file_size)}".encode())
        time.sleep(0.01)
        file = open(file_name, "rb")
        data = file.read()
        client.sendall(data)
        file.close()
        print(client.recv(1024).decode())

def descargar():
    client.send(f'<DOWNLOAD>'.encode())
    print(client.recv(1024).decode())
    time.sleep(0.01)
    file_name = args.download
    client.send(file_name.encode())
    print(client.recv(1024).decode())
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
    print(client.recv(1024).decode())
    time.sleep(0.01)
    client.send(file.encode())
    print(client.recv(1024).decode())
    client.close()

def enviarCredenciales(user, pwd):
    client.send(f'{user}|{pwd}'.encode())
    print(client.recv(1024).decode())
    
def modificarPermisos(user, permisos):
    time.sleep(0.01)
    client.send(f'{user}|{permisos}'.encode())
    print(client.recv(1024).decode())

if __name__ == '__main__':

    parser = argparse.ArgumentParser("Terminal del cliente")
    parser.add_argument('user', type=str, help='Indica el usuario')
    parser.add_argument('pwd', type=str, help='Indica la contraseña')
    parser.add_argument('-f', '--file', type=str, nargs='+', help='Especifica la ruta o archivos que se va a enviar')
    parser.add_argument('-l', '--list', action='store_true', help='Devuelve un listado de los archivos en el servidor')
    parser.add_argument('-d', '--download', type=str, help='Descarga el archivo especificado')
    parser.add_argument('-r', '--remove', type=str, help='Elimina el archivo especificado en el servidor remoto')
    parser.add_argument('-m', '--modify', nargs=2, type=str, help='Indicar usuario y nivel de permiso que se le va a asignar')
    args = parser.parse_args()

    enviarCredenciales(args.user, args.pwd)

    if args.user == 'admin' and args.modify:
        client.send(f'<MODIFY>'.encode())
        usuario, permisos = args.modify
        modificarPermisos(usuario, permisos)
    elif args.modify:
        print('Solo el administrador puede modificar permisos')

    try:
        if args.list:
            listar()

        if args.file:
            client.send(f'<POST>'.encode())
            msg = client.recv(1024).decode()
            if 'DENEGADO' in msg:
                print(msg)
                client.close()
            else:
                print(msg)
                client.send(f'{len(args.file)}'.encode())
                time.sleep(0.01)
                enviar()

        if args.download:
            descargar()

        if args.remove:
            borrar()

    except ValueError:
        pass
