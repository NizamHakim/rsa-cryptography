import socket
import des
import json
import rsa
import pkauthority

HOST = '127.0.0.1'
PORT = 5001
PUBLIC_KEY = {'n': 5063, 'd': 4561}
PRIVATE_KEY = {'n': 5063, 'e': 3481}

def client_program():
    KEY = 'aBhNDJjB'
    client_socket = createSocket()
    server_address = ('127.0.0.1', 5000)
    client_socket = handshake(client_socket, server_address, KEY)

    try:
        while True:
            message = input("message to send: ")
            encryptedMessage = des.cbcEncrypt(message, KEY, KEY[::-1]) # CBC mode
            print(f"sending encrypted message: {encryptedMessage}")
            client_socket.send(encryptedMessage.encode('utf-8'))
            
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Received response: {response}")
            decryptedResponse = des.cbcDecrypt(response, KEY, KEY[::-1])
            print(f"Decrypted response: {decryptedResponse}")
            
    except KeyboardInterrupt:
        print('Client shutting down ...')
        client_socket.close()

def handshake(client_socket, server_addr, key):
    pka_address = ('127.0.0.1', 6000)
    pka_public_key = {'n': 1073, 'd': 509}
    
    print(f"Sending request to PKA for server public key ...")
    client_socket.connect(pka_address)
    client_socket.send(str(server_addr).encode('utf-8'))
    server_public_key = client_socket.recv(1024).decode('utf-8')
    server_public_key = rsa.decrypt(server_public_key, pka_public_key)
    server_public_key = json.loads(server_public_key)
    client_socket.close()
    print(f"Received server public key: {server_public_key}")
    
    print(f"Initiating handshake with server ...")
    client_socket = createSocket()
    client_socket.connect(server_addr)
    key = rsa.encrypt(key, PRIVATE_KEY)
    client_socket.send(key.encode('utf-8'))    
    response = client_socket.recv(1024).decode('utf-8')
    if response == 'ACK':
        print('Handshake successful.')
        return client_socket
    
def createSocket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.bind((HOST, PORT))
    return client_socket
    
    

if __name__ == '__main__':
    client_program()