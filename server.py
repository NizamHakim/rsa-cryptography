import socket
import des
import rsa
import json
import select

HOST = '127.0.0.1'
PORT = 5000
PUBLIC_KEY = {'n': 3139, 'd': 673}
PRIVATE_KEY = {'n': 3139, 'e': 337}

def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    
    print(f"Listening on {HOST}:{PORT} ...")
    
    input_socket = [server_socket]
    key = None
    try:
        while True:
            read_ready, _, _ = select.select(input_socket, [], [])
            
            for sock in read_ready:
                if sock == server_socket:
                    client_socket, addr = server_socket.accept()
                    print(f"Connection from client {addr}")
                    input_socket.append(client_socket)
                    key = handshake(client_socket, addr)
                else:            	
                    data = sock.recv(1024).decode('utf-8')
                
                    if data:
                        print(f"Received message: {data}")
                        decrypted_data = des.cbcDecrypt(data, key, key[::-1])
                        print(f"Decrypted message: {decrypted_data}")
                        
                        response = input("Enter response: ")
                        response = des.cbcEncrypt(response, key, key[::-1])
                        sock.send(response.encode('utf-8'))
                        print(f"sending encrypted response: {response}")
                    else:                    
                        sock.close()
                        input_socket.remove(sock)
                        key = None
                    
            
    except KeyboardInterrupt:
        print("Server shutting down.")
        server_socket.close()
    
def handshake(server_socket, client_addr):
    pka_address = ('127.0.0.1', 6000)
    pka_public_key = {'n': 1073, 'd': 509}
    
    print(f"Sending request to PKA for client public key ...")
    server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket2.connect(pka_address)
    server_socket2.send(str(client_addr).encode('utf-8'))
    client_public_key = server_socket2.recv(1024).decode('utf-8')
    client_public_key = rsa.decrypt(client_public_key, pka_public_key)
    client_public_key = json.loads(client_public_key)
    server_socket2.close()
    print(f"Received client public key: {client_public_key}")
    
    print(f"Responding to client handshake to obtain key ...")
    key = server_socket.recv(1024).decode('utf-8')
    key = rsa.decrypt(key, client_public_key)
    print(f"Received key: {key}")
    server_socket.send("ACK".encode('utf-8'))
    return key

if __name__ == '__main__':
    server_program()