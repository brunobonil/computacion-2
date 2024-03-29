import socket


HOST = '192.168.100.156'
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
    com_socket.send(f'Received'.encode('utf-8'))
    com_socket.close()
    print(f'Connection ended')


