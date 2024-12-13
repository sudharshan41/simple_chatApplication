import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received: {message}")
                broadcast(message, client_socket)
            else:
                break
        except:
            break

    # Remove client from the list and close the connection
    clients.remove(client_socket)
    client_socket.close()

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)
                client.close()

# Create and bind the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.56.1', 5555))  # Your server IP and port
server.listen(5)
print("Server is listening on 192.168.56.1:5555...")

clients = []

while True:
    client_socket, addr = server.accept()
    print(f"Connection from {addr}")
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket,)).start()
