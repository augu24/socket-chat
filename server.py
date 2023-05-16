from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

import sys
import errno

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
    username = client.recv(4096).decode()
    username = decrypter(username, d)
    client.send(encrypter(f"{username} vient de rejoindre le serveur.", d).encode())
    repeteur(f"{username} vient de rejoindre.")
    clients[client] = username

    while True:
        message = client.recv(4096).decode()
        message = decrypter(message, d)
        repeteur(message, username+": ")

def accepteConnexion():
    while True:
        client, addrClient = server.accept()
        print(f"{addrClient[1]} vient de se connecter.")
        messBienvenue = encrypter("Bienvenue sur Socket Chat! Merci de rentrer votre nom d'utilisateur:", d)
        client.send(messBienvenue.encode())
        addresses[client] = addrClient
        Thread(target=manageClient, args=(client,)).start() #args=(client,) car args doit etre tuple et (variable,) la virgule marque une tuple de length 1


def repeteur(message, prefix=""):
    message = prefix+message
    message = encrypter(message, d)
    try:
        for soket in clients:
            soket.send(message.encode())
    except IOError as e:
        if e.errno == errno.EPIPE:
            pass


clients = {}
addresses = {}

port = 8080
host = "127.0.0.1"

server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))
server.listen()

print("En attente de connexion ...")
accepte_thread = Thread(target=accepteConnexion)
accepte_thread.start()
accepte_thread.join()
server.close()

    
