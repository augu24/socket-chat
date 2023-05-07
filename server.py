from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

def manageClient(client): 
    username = client.recv(1024).decode("utf8")
    client.send(bytes(f"{username} vient de rejoindre le serveur.", "utf8"))
    repeteur(bytes(f"{username} vient de rejoindre.", "utf8"))
    clients[client] = username

    while True:
        message = client.recv(1024)
        repeteur(message, username+": ")

def accepteConnexion():
    while True:
        client, addrClient = server.accept()
        print(f"{addrClient[1]} vient de se connecter.")
        client.send(bytes("Bienvenue sur Socket Chat! Merci de rentrer votre nom d'utilisateur:", "utf8"))
        addresses[client] = addrClient
        Thread(target=manageClient, args=(client,)).start()


def repeteur(message, prefix=""):
    for soket in clients:
        soket.send(bytes(prefix, "utf8")+message)

port = 8080
host = "127.0.0.1"
addr = (host, port)

server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)
server.listen()
print("En attente de connexion ...")
accepte_thread = Thread(target=accepteConnexion)
accepte_thread.start()
accepte_thread.join()
server.close()



    
