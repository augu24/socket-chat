
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

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

def envoyer():
    message = monMess.get()
    monMess.set("")
    message = encrypter(message, d)
    socketClient.send(bytes(message, "utf8"))


def recevoir():
    while True:
        try:
            message = socketClient.recv(1024).decode("utf8")
            message = decrypter(message, d)
            listeMess.insert(tkinter.END, message)
        except:  
            break

def fermeture():
    socketClient.close()
    top.quit()

top = tkinter.Tk()

top.title("Socket Chat")
screen_x = int(top.winfo_screenwidth())
screen_y = int(top.winfo_screenheight())
top.geometry(f"700x480+{screen_x// 2 - 350}+{screen_y// 2 - 300}")
top.configure(bg="black")
top.protocol("WM_DELETE_WINDOW", fermeture)

cadreMess = tkinter.Frame(top)
monMess = tkinter.StringVar() 
monMess.set("")
scrollbar = tkinter.Scrollbar(cadreMess)
scrollbar = tkinter.Scrollbar(cadreMess)
listeMess = tkinter.Listbox(cadreMess, height=15, width=50, yscrollcommand=scrollbar.set,fg="green",  highlightthickness=3, highlightbackground="green", highlightcolor="green")
listeMess.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
listeMess.configure(bg="black")
listeMess.pack()
cadreMess.pack()
champs = tkinter.Entry(top, textvariable=monMess,fg = "green", bg = "black",highlightbackground="green",insertbackground="green")
champs.bind("<Return>", envoyer)
champs.pack(pady=(10,0))
texte = tkinter.Label(top, text="Envoyer (⏎)", fg='green',bg = "black")
texte.pack()

port = 8080
host = "127.0.0.1" 

socketClient = socket(AF_INET, SOCK_STREAM)
socketClient.connect((host, port))
recevoir_thread = Thread(target=recevoir)
recevoir_thread.start()
tkinter.mainloop() 
## print("Une erreur est survenu, veuilliez reesayer.")
