import socket
import utility as u

        
HOST = u.get_ip()
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))

server.listen()

while True:
    com_socket, address = server.accept()

    print(f'Connected to {address}')
    message = com_socket.recv(1024).decode('utf-8')
    print(f'Message is: {message}')
    com_socket.send(input("Mensaje para el cliente: ").encode('utf-8'))
    print(com_socket.recv(1024).decode('utf-8'))
        

