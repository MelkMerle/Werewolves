# coding=utf-8

import socket, struct
from Plateau import PlateauDeJeu
Intelligence

class NetworkManager:

    def __init__(self):
        self.game_over = 0
        # Création de la socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Récupération en ligne de commande l'addresse ip et le port
        self.ip = input("Adresse IP du serveur : ")
        self.port = int(input("Port :"))
        # Connexion de la socket
        try:
            self.sock.connect((self.ip, self.port))
        except Exception as error:
            print("Connection error: ", error)

        # Autres Initialisations
        self.Plateau = PlateauDeJeu() #initialisation de la map, avec 0 ligne, 0 colonnes, 0 maisons, 0 humains, 0 vampires, 0 LG
        #le plateau de jeu en lui meme est un tableau nxm, avec à chaque case carte[x][y] = [<lettre de l'espèce>, nombre de l'espèce]
        self.IA = Intelligence(self.Plateau) #initialisation de l'heuristique à développer (bien mettre tout à 0 pour la réinitialisation)

    def send(self, *messages):
        """Send a given set of messages to the server."""
        for message in messages:
            try:
                if(isinstance(message, int)):
                    data = struct.pack('=B', message)
                elif (isinstance(message, str)):
                    data = bytes(message, 'utf-8')
                else:
                    print(message)
                print(data);
                self.sock.send(data)
            except error:
                print("Couldn't send message: ", message, error)

    def recv(self, length):
        return struct.unpack('=B',self.sock.recv(length))


    def update(self):
        primitiveOrder = self.sock.recv(3) #pas décodé
        order = primitiveOrder.decode("utf-8")
        if not order:
            print("Bizarre, c'est vide")

        if order == "UPD":
            #mettez à jour votre Plateau à partir des tuples contenus dans changes
            n = self.recv(1)[0]
            changes = []
            for i in range(n):
                for j in range(5):
                    changes.append(self.recv(1)[0]) # chaque change a la forme [X, Y, nombre_H, nombre_V, nombre_L]
            for change in changes:
                x = change[0]
                y = change[1]
                humains=change[2]
                vamp=change[3]
                lg=change[4]
                if humains>0:
                    self.Plateau.carte[x][y]=['H', humains]
                elif vamp>0:
                    self.Plateau.carte[x][y]=['V', vamp]
                elif lg>0:
                    self.Plateau.carte[x][y]=['L', lg]
                else:
                    self.Plateau.carte[x][y]=['O', 0]

            #calculez votre coup
            IA.calculDuCoup() #calcule la variable interne "coup" de l'IA, qui est un tableau de Nx5 chiffres(x_dep,y_dep,nombre,x_arr,y_arr)_
            #préparez la trame MOV ou ATK
            self.send("MOV", IA.coup)

        elif order == "SET":
            lines = (self.recv(1)[0])
            columns = (self.recv(1)[0])
            print("J'ai recu SET")
            self.IA.lignes = lines
            self.IA.colonnes = columns

        elif order == "HUM":
           print "commande dépréciée"

        elif order == "HME":
            x = self.recv(1)[0]
            y = self.recv(1)[0]
            self.IA.maMaison = [x, y]

        elif order == "MAP":
            n = self.recv(1)[0]
            changes = []
            for i in range(n):
                changement=[]
                for j in range(5): #devrait changer avec la forme self.recv(5)[0]
                    changement.append(self.recv(1)[0]) # chaque change a la forme [X, Y, nombre_H, nombre_V, nombre_L]
                changes.append(changement)
            for change in changes:
                x = change[0]
                y = change[1]
                humains=change[2]
                vamp=change[3]
                lg=change[4]
                # if humains>0:
                #     self.Plateau.carte[x][y]=['H', humains]
                # elif vamp>0:
                #     self.Plateau.carte[x][y]=['V', vamp]
                # elif lg>0:
                #     self.Plateau.carte[x][y]=['L', lg]
                # else:
                #     self.Plateau.carte[x][y]=['O', 0]

                for group in self.Plateau.groupes



        elif order == "END":
            self.Plateau = Map() #réinitialise le Plateau
            self.IA = Intelligence() #réinitialise l' IA
            #ici on met fin à la partie en cours
            #Réinitialisez votre modèle

        elif order == "BYE":
            self.sock.close()
            #autres choses à faire pour la mise en fin
            self.game_over=1
        else:
            print("commande non attendue recue", order)