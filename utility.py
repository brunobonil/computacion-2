import socket


def get_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Connect to a well-known address to get local IP address
        s.connect(("8.8.8.8", 80))
        
        # Get the local IP address
        ip_address = s.getsockname()[0]
        
        # Close the socket
        s.close()
        
        return ip_address
    
    except Exception as e:
        print(f'Error: {e}')
        
        return None