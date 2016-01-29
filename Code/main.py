# coding=utf-8
import struct
from network_manager import NetworkManager

#à mettre en attributs d'une classe Map
#lignes = 0
#colonnes = 0


#only for testing purposes
ip = "127.0.0.1"
port = int(5555)

# Lancement du network manager
manager = NetworkManager()


#Envoi du nom
groupname = "Les loups bleus"
manager.send('NME', len(groupname), groupname)


#boucle principale
while True:
    manager.update()
    if manager.game_over == 1:
        print "Bye bye."
        break
# faut-il faire quelque chose pour que le programme quitte ?