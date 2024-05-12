import datetime as dt
import time
import socket
import tqdm
import utility
import os
import multiprocessing as mp
import json

def list_files(user, addr, conn):
        client.send('Permiso para LISTAR verificado. Listando archivos...'.encode())
        time.sleep(0.01)
        files_list = os.listdir('./shared_files_folder')
        files_list_bytes = b'|'.join([i.encode() for i in files_list])
        client.send(f'{len(files_list_bytes)}'.encode())
        time.sleep(0.01)
        client.send(files_list_bytes)
        conn.send(f'La terminal {addr} ha listado los archivos | {dt.datetime.now()}')

def recv_file(user, addr, conn):
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

def send_file(user, addr, conn):
    file_name = client.recv(1024).decode()
    file = open(f'./shared_files_folder/{file_name}', "rb")
    file_bytes = file.read()
    file_to_send = (str(len(file_bytes))+'|||').encode()
    file_to_send += file_bytes
    client.sendall(file_to_send)
    file.close()
    if client.recv(1024).decode():
        conn.send(f'La terminal {addr} ha descargado archivo(s) | {dt.datetime.now()}')

def remove_file(user, addr, conn):
        client.send('Permiso para eliminar archivo concedido'.encode())
        file_name = client.recv(1024).decode()
        print(file_name)
        try:
            os.remove(f'./shared_files_folder/{file_name}')
            client.send(f'El archivo se ha eliminado exitosamente'.encode())
        except FileNotFoundError:
            client.send(f'El archivo no existe.'.encode())
        conn.send(f'La terminal {addr} ha eliminado archivos | {dt.datetime.now()}')
        
def logger(conn):
    while True:    
        log = conn.recv()
        logFile = open('./server_logger.txt', 'ab')
        logFile.write(f'{log}\n{"="*100}\n'.encode())
        logFile.close()

def modify_permissions(addr, conn):

    user, permiso = client.recv(1024).decode().split('|')
    if len(permiso) != 4 or any(i not in ['1','0'] for i in permiso):
        client.send('El formato de permiso no es correcto'.encode())
        client.close()
        return
    with open("users.json", "r") as archivo:
        usuarios = json.load(archivo)
    
    try:
        usuarios[user]['permisos'] = permiso
        archivo = open('users.json', 'w')
        json.dump(usuarios, archivo, indent=4)    
        client.send(f'Se han modificado los permisos del usuario {user} correctamente'.encode())
        client.close()
        return
    except KeyError:
        client.send(f'El usuario indicado no existe, intentar nuevamente'.encode())
        client.close()
    

def autenticador(client):
    # Esquema de permisos: 4 bits -> 1º: listar, 2º cargar, 3º descargar, 4º eliminar
    try:
        user, pwd = client.recv(1024).decode().split('|')
    except ValueError:
        return False # Sale de la funcion por falta de valores
    with open("users.json", "r") as archivo:
        datos = json.load(archivo)
    try:
        if datos[user]["pwd"] == pwd:         
            client.send("Acceso PERMITIDO".encode())
            return user
        else:
            client.send('Acceso DENEGADO. Contraseña incorrecta'.encode())
            return False
    except KeyError:
        client.send("El usuario no está registrado. Registrando credenciales...".encode())
        datos[user] = {"pwd": pwd, "permisos": "1000"} # Por defecto tienen permiso de listar archivos unicamente
        with open('users.json', "w") as archivo:
            json.dump(datos, archivo, indent=4)
        return user
        

def method(req_type, addr, conn, user):
        with open("users.json", "r") as archivo:
                datos = json.load(archivo)

        if req_type == '<GET>':
            if not int(datos[user]["permisos"][0]):
                client.send("No tiene permiso para listar archivos".encode())
                return
            list_files(user, addr, conn)
            
        if req_type == '<POST>':
            if not int(datos[user]["permisos"][1]):
                client.send("No tiene permiso para subir archivos".encode())
                return
            while True:
                recv_file(user, addr, conn)

        if req_type == '<DOWNLOAD>':
            if not int(datos[user]["permisos"][2]):
                client.send("No tiene permiso para descargar archivos".encode())
                return
            send_file(user, addr, conn)

        if req_type == '<REMOVE>':
            if not int(datos[user]["permisos"][3]):
                client.send("No tiene permiso para eliminar archivos".encode())
                return
            remove_file(user, addr, conn)
        
        if req_type == '<MODIFY>':
            modify_permissions(addr, conn)
        client.close()


if __name__ == '__main__':
    
    HOST = utility.get_ip()
    PORT = 9090
    # Meter autenticación de clientes
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Especificar el tipo de conexión IPV4 o IPV6
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    parent_conn, child_conn = mp.Pipe()
    l = mp.Process(target=logger, args=(child_conn,))
    l.start()

    while True:            
        client, address = server.accept()
        print(f'Connected to {address}')
        user = autenticador(client)
        if user == False: client.close(); continue # Si falla la autenticacion por falta de valores, se corta la conexion
        
        req_type = client.recv(1024).decode()
        p = mp.Process(target=method, args=(req_type, address[0], parent_conn, user))
        p.start()
        client.close()        

