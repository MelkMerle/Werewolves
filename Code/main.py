# coding=utf-8
import socket, struct


def send(sock, *messages):
    """Send a given set of messages to the server."""
    for message in messages:
        try:
            
            if(isinstance(message, int)):
                data = struct.pack('=B', message)
            elif (isinstance(message, str)):
                data = bytes(message)
            else:
                print(message)
            print(data);
            sock.send(data)
        except Exception as error :
            print("Couldn't send message: ", message, error)

lignes = 0
colonnes = 0

#Création de la socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Récupération en ligne de commande l'addresse ip et le port
# ip = input("Adresse IP du serveur : ")
# port = int(input("Port :"))

ip = "172.20.10.4"
port = int(5555)

#Connexion de la socket
try:
    sock.connect((ip, port))
except Exception as error:
    print("Connection error: ", error)

#Envoi du nom
groupname = "Les loups bleus"
send(sock, 'NME', len(groupname), groupname)


#boucle principale
while True:
    primitiveOrder = sock.recv(3) #pas décodé
    order = primitiveOrder.decode("utf-8")
    if not order:
        print("Bizarre, c'est vide")

    if order == "SET":
        lignes = (struct.unpack('=B', sock.recv(1))[0])
        colonnes = (struct.unpack('=B', sock.recv(1))[0])
        print("J'ai recu SET")
        #ici faire ce qu'il faut pour préparer votre représentation
        #de la carte
    elif order == "HUM":
        n = struct.unpack('=B', sock.recv(1))[0]
        maisons = []
        for i in range(n):
            maisons.append((struct.unpack('=B', sock.recv(1))[0] for i in range(2)))
        #maisons contient la liste des coordonnées des maisons
        #ajoutez votre code ici
    elif order == "HME":
        x, y = (struct.unpack('=B', sock.recv(1))[0] for i in range(2))
        #ajoutez le code ici (x,y) étant les coordonnées de votre
        #maison
    elif order == "UPD":
        n = struct.unpack('=B', sock.recv(1))[0]
        changes = []
        for i in range(n):
            changes.append((struct.unpack('=B', sock.recv(1))[0] for i in range(5)))
        #mettez à jour votre carte à partir des tuples contenus dans changes
        #calculez votre coup
        #préparez la trame MOV ou ATK
        #Par exemple:
        send(sock, "MOV", 1,2,1,1,3)
    elif order == "MAP":
        n = struct.unpack('=B', sock.recv(1))[0]
        changes = []
        for i in range(n):
            changes.append((struct.unpack('=B', sock.recv(1))[0] for i in range(lignes*colonnes)))
        #initialisez votre carte à partir des tuples contenus dans changes
    elif order == "END":
        lignes = 0;
        colonnes = 0;
        #ici on met fin à la partie en cours
        #Réinitialisez votre modèle
    elif order == "BYE":
        #coucou
        break
    else:
        print("commande non attendue recue", order)

#Préparez ici la déconnexion
                
#Fermeture de la socket
    sock.close()






