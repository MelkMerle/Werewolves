# coding=utf-8

import socket, struct

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
        self.gameBoard = PlateauDeJeu() #initialisation de la map, avec 0 ligne, 0 colonnes, 0 maisons, 0 humains, 0 vampires, 0 LG
        #le plateau de jeu en lui meme est un tableau nxm, avec à chaque case carte[x][y] = [<lettre de l'espèce>, nombre de l'espèce]
        self.IA = Intelligence() #initialisation de l'heuristique à développer (bien mettre tout à 0 pour la réinitialisation)

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
            #mettez à jour votre gameBoard à partir des tuples contenus dans changes
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
                    self.gameBoard.carte[x][y]=['H', humains]
                elif vamp>0:
                    self.gameBoard.carte[x][y]=['V', vamp]
                elif lg>0:
                    self.gameBoard.carte[x][y]=['L', lg]
                else:
                    self.gameBoard.carte[x][y]=['O', 0]

            #calculez votre coup
            IA.calculDuCoup() #calcule la variable interne "coup" de l'IA, qui est un tableau de Nx5 chiffres(x_dep,y_dep,nombre,x_arr,y_arr)_
            #préparez la trame MOV ou ATK
            self.send("MOV", IA.coup)

        elif order == "SET":
            lines = (self.recv(1)[0])
            columns = (self.recv(1)[0])
            print("J'ai recu SET")
            self.gameBoard.lignes = lines
            self.gameBoard.colonnes = columns

        elif order == "HUM":
            n = self.recv(1)[0]
            for i in range(n):
                #je ne comprends pas bien comment fonctionne sock.recv, et pourquoi il faut un [0] partout, du coup j'ai fait ça, plutot que self.recv(2) sans boucle sur j... à discuter
                for j in range(2):
                    self.gameBoard.maisons.append(self.recv(1)[0])
            print self.gameBoard.maisons

        elif order == "HME":
            x = self.recv(1)[0]
            y = self.recv(1)[0]
            self.gameBoard.maMaison = [x, y]

        elif order == "MAP":
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
                    self.gameBoard.carte[x][y]=['H', humains]
                elif vamp>0:
                    self.gameBoard.carte[x][y]=['V', vamp]
                elif lg>0:
                    self.gameBoard.carte[x][y]=['L', lg]
                else:
                    self.gameBoard.carte[x][y]=['O', 0]

        elif order == "END":
            self.gameBoard = Map() #réinitialise la gameBoard
            self.IA = Intelligence() #réinitialise l' IA
            #ici on met fin à la partie en cours
            #Réinitialisez votre modèle

        elif order == "BYE":
            self.sock.close()
            #autres choses à faire pour la mise en fin
            self.game_over=1
        else:
            print("commande non attendue recue", order)