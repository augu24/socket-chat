from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

global d
d = 11

def encrypter(texte, decalage):
    resultat = ""
    for char in texte:
        if char.isupper():
            resultat += chr((ord(char) + decalage - 65) % 26 + 65)
        elif char.islower():
            resultat += chr((ord(char) + decalage - 97) % 26 + 97)
        else:
            resultat += char
    return resultat

def decrypter(texte_chiffre, decalage):
    resultat = ""
    for char in texte_chiffre:
        if char.isupper():
            resultat += chr((ord(char) - decalage - 65) % 26 + 65)
        elif char.islower():
            resultat += chr((ord(char) - decalage - 97) % 26 + 97)
        else:
            resultat += char
    return resultat

def manageClient(client): 
    username = client.recv(1024).decode("utf8")
    username = decrypter(username, d)
    client.send(bytes(encrypter(f"{username} vient de rejoindre le serveur."),d), "utf8")
    repeteur(f"{username} vient de rejoindre.")
    clients[client] = username

    while True:
        message = client.recv(1024)
        message = decrypter(message, d)
        repeteur(message, username+": ")

def accepteConnexion():
    while True:
        client, addrClient = server.accept()
        print(f"{addrClient[1]} vient de se connecter.")
        messBienvenue = encrypter("Bienvenue sur Socket Chat! Merci de rentrer votre nom d'utilisateur:", d)
        client.send(bytes(messBienvenue, "utf8"))
        addresses[client] = addrClient
        Thread(target=manageClient, args=client).start()


def repeteur(message, prefix=""):
    message = encrypter(message, d)
    if prefix != "":
        avant = encrypter(prefix, d)
    else:
        avant=""
    for soket in clients:
        soket.send(bytes((avant+message), "utf8"))

clients = {}
addresses = {}

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

    
