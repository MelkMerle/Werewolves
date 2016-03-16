# coding=utf-8
from network_manager import NetworkManager
import sys

#à mettre en attributs d'une classe Map
#lignes = 0
#colonnes = 0


#only for testing purposes
cmd = sys.argv[1:]
print(cmd)
assert len(cmd) ==2 #verifier qu'on a bien seulement 2 arguments
ip, port = cmd

# Lancement du network manager
manager = NetworkManager(ip, int(port))


#Envoi du nom
groupname = "Les vampires rouges"
manager.send('NME', len(groupname), groupname)


#boucle principale
while True:
    manager.update()
    if manager.game_over == 1:
        print("Bye bye.")
        break

# faut-il faire quelque chose pour que le programme quitte ?
