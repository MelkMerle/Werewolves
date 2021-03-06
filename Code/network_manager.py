﻿# coding=utf-8

import socket, struct
from Plateau import PlateauDeJeu
from IA import Intelligence
from species import Species

class NetworkManager:

    def __init__(self, ip, port):
        self.game_over = 0
        # Création de la socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Récupération de l'addresse ip et le port
        self.ip = ip
        self.port = port

        # Connexion de la socket
        try:
            self.sock.connect((self.ip, self.port))
        except Exception as error:
            print("Connection error: ", error)

        # Autres Initialisations
        self.Plateau = PlateauDeJeu() # initialisation de la map, avec 0 ligne, 0 colonnes, 0 maisons, 0 humains, 0 vampires, 0 LG
        # le plateau de jeu est un simple tableau d'instances de la classe Groupe
        self.IA = Intelligence() # initialisation de l'IA

    def send(self, *messages):
        """Send a given set of messages to the server."""
        for message in messages:
            try:
                if(isinstance(message, int)):
                    data = struct.pack('=B', message)
                elif (isinstance(message, str)):
                    data = bytes(message, 'utf-8')
                elif (isinstance(message, list)):
                    for mess in message:
                        self.send(mess)
                    return
                else:
                    print("couldn't pack message: ", message)
                self.sock.send(data)
            except Exception as error:
                print("Couldn't send message: ", message, error)

    def recv(self, length):
        returnTable=[]
        for i in range(length):
            returnTable.append(struct.unpack('=B', self.sock.recv(1))[0])
        return returnTable


    def update(self):
        primitiveOrder = self.sock.recv(3) # pas décodé
        order = primitiveOrder.decode("utf-8")
        if not order:
            print("Bizarre, c'est vide")

        if order == "UPD":
            # mettez à jour votre Plateau à partir des tuples contenus dans changes
            print("j'ai reçu UPD")
            n = self.recv(1)[0]
            changes = []
            for i in range(n):
                changement=self.recv(5)  # chaque changement a la forme [X, Y, nombre_H, nombre_V, nombre_L]
                self.updateGroups(changement)

            # calculez votre coup, c'est ici le coeur de l'aglo
            coup = self.IA.chooseMission(self.Plateau)
            # calcule le coup de l'IA, qui est un tableau de
                              # Nx5 chiffres(x_dep,y_dep,nombre,x_arr,y_arr)_
            # préparez la trame MOV ou ATK
            self.send("MOV", coup)

        elif order == "SET":
            lines = (self.recv(1)[0])
            columns = (self.recv(1)[0])
            print("J'ai recu SET")
            self.Plateau.height = lines
            self.Plateau.width = columns

        elif order == "HUM":
           n = self.recv(1)[0]
           for i in range(n):
                for j in range(2):
                    self.recv(1)[0] #on depile juste la socket mais c'est un ordre déprécié

        elif order == "HME":
            x = self.recv(1)[0]
            y = self.recv(1)[0]
            print("J'ai reçu HME :", x,y)
            self.Plateau.maMaison = [x, y]

        elif order == "MAP":
            n = self.recv(1)[0]
            changes = []
            for i in range(n):
                changement=self.recv(5)
                changes.append(changement)
            for changement in changes:
                x = changement[0]
                y = changement[1]
                humains=changement[2]
                vamp=changement[3]
                lg=changement[4]
                if humains>0:
                    self.Plateau.addGroup(x,y,humains,Species.human)
                elif vamp>0:
                    self.Plateau.addGroup(x,y,vamp,Species.vampire)
                elif lg>0:
                    self.Plateau.addGroup(x,y,lg,Species.werewolf)
                else :
                    print("espèce non attendue reçue en commande MAP")
            myGroupe = self.Plateau.getGroup(self.Plateau.maMaison[0],self.Plateau.maMaison[1])
            self.IA.mySpecie = myGroupe.species


        elif order == "END":
            self.Plateau = PlateauDeJeu() # réinitialise le Plateau
            self.IA = Intelligence() # réinitialise l' IA

        elif order == "BYE":
            self.sock.close()
            self.game_over=1
        else:
            print("commande non attendue recue", order)

    def updateGroups(self, change):
            x = change[0]
            y = change[1]
            num_humans = change[2]
            num_vamp = change[3]
            num_wolves = change[4]
            effectif = 0
            espece = None
            # détermination de l'espèce concernée par le changement
            if num_humans > 0:
                effectif = num_humans
                espece = Species.human
            elif num_vamp > 0:
                effectif = num_vamp
                espece = Species.vampire
            elif num_wolves > 0:
                effectif = num_wolves
                espece = Species.werewolf
            elif num_humans == 0 and num_vamp == 0 and num_wolves == 0:
                effectif = 0
            else:
                print("espèce non attendue reçue en commande UPD")

            # parcours des groupes et mise à jour du bon
            notfound = 1
            for group in self.Plateau.groupes:
                if group.x == x and group.y == y:
                    notfound = 0
                    if effectif == 0:
                        self.Plateau.groupes.remove(group)
                    else:
                        group.eff = effectif
                        group.species = espece
                    break
            # si on a pas trouvé de groupe correspondant, on le crée
            if notfound:
                self.Plateau.addGroup(x, y, effectif, espece)
