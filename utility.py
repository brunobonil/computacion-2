import socket


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create a socket object
        s.connect(("8.8.8.8", 80)) # Connect to a well-known address to get local IP address
        ip_address = s.getsockname()[0] # Get the local IP address
        s.close() # Close the socket
        return ip_address
    
    except Exception as e:
        print(f'Error: {e}')
        return None