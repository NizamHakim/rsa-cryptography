import socket
import rsa
import json\

HOST = '127.0.0.1'
PORT = 6000
PUBLIC_KEY = {'n': 1073, 'd': 509}
PRIVATE_KEY = {'n': 1073, 'e': 101}

PKA_DATABASE = {
    "('127.0.0.1', 5000)": { 'n': 3139, 'd': 673 },
    "('127.0.0.1', 5001)": { 'n': 5063, 'd': 4561 }
}

def handle_client_connection(client_socket):
    print(f"Connection from {client_socket.getpeername()}")
    request_key = client_socket.recv(1024).decode('utf-8')
    
    print(f"Looking up public key for {request_key} ...")
    response = PKA_DATABASE.get(str(request_key))
    print(f"Found public key: {response}")
    response = json.dumps(response)
    response = rsa.encrypt(response, PRIVATE_KEY)
    client_socket.send(response.encode('utf-8')) 
    print(f"Sending public key to client ...")


def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    
    print(f"Listening on {HOST}:{PORT} ...")
    
    try:
        while True:
            client_socket, addr = server_socket.accept()
            handle_client_connection(client_socket)
            
    except KeyboardInterrupt:
        print("Server shutting down.")
        server_socket.close()
        

if __name__ == '__main__':
    server_program()