import threading
import socket

host = "localhost"
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} has left the game!".encode("ascii"))
            nicknames.remove(nickname)
            break

def recieve():
    while True:
        client, address = server.accept()
        print(f"Connection from {str(address)}")

        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client is {nickname}!")

        broadcast(f"{nickname} has joined the game!".encode("ascii"))
        client.send("Connected to the server!".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is running!")
recieve()
