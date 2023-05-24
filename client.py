
from socket import AF_INET, socket, SOCK_STREAM 
#AF_INET = type d'addresse ici l'IP sera alors une string et le port un entier
#SOCKET_STREAM = type de socket ici correspond au type TCP

from threading import Thread
import tkinter

global d
d = 11


def on_enter(event):
    texte.config(bg='green', fg='black')

def on_leave(event):
    texte.config(bg='black', fg='green')

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

def envoyer(event=None):
    message = monMess.get()
    monMess.set("")
    message = encrypter(message, d)

    socketClient.send(message.encode())


def recevoir():
    while True:
        try:

            message = socketClient.recv(4096).decode()

            message = decrypter(message, d)
            listeMess.insert(tkinter.END, message)
        except:  
            break

def fermeture():
    socketClient.send(encrypter("vient de quitter.").encode())
    socketClient.close()
    top.quit()

top = tkinter.Tk()

top.title("Socket Chat")
screen_x = int(top.winfo_screenwidth())
screen_y = int(top.winfo_screenheight())
top.geometry(f"700x480+{screen_x// 2 - 350}+{screen_y// 2 - 300}")
top.configure(bg="black")
global titre
titre = tkinter.Label(top, text = "Bienvenue sur pychat !",bg = "Black", fg = "green", font = ("Courier",30))
top.protocol("WM_DELETE_WINDOW", fermeture)

cadreMess = tkinter.Frame(top)
monMess = tkinter.StringVar() 
monMess.set("")
scrollbar = tkinter.Scrollbar(cadreMess)
scrollbar = tkinter.Scrollbar(cadreMess)
listeMess = tkinter.Listbox(cadreMess, height=15, width=50, yscrollcommand=scrollbar.set,fg="green",  highlightthickness=3, highlightbackground="green", highlightcolor="green")
listeMess.configure(bg="black")
champs = tkinter.Entry(top, textvariable=monMess,fg = "green", bg = "black",highlightbackground="green",insertbackground="green")
champs.bind("<Return>", envoyer)
texte = tkinter.Label(top, text="Envoyer (⏎)", fg='green',bg = "black")
texte.bind("<Button-1>",lambda event:envoyer())
texte.bind("<Enter>",on_enter )
texte.bind("<Leave>",on_leave)

port = 8080
host = "127.0.0.1" 
try:

    socketClient = socket(AF_INET, SOCK_STREAM)
    socketClient.connect((host, port))

    recevoir_thread = Thread(target=recevoir)
    recevoir_thread.start()

    titre.pack(pady=(20,10))
    listeMess.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    cadreMess.pack()
    champs.pack(pady=(10,0))
    texte.pack()
    tkinter.mainloop() 

except:
    print("Une erreur est survenu.")

