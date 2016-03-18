# coding=utf-8
from network_manager import NetworkManager
import sys

cmd = sys.argv[1:]
assert len(cmd) ==2  #verifier qu'on a bien seulement 2 arguments
ip, port = cmd

# Lancement du network manager
manager = NetworkManager(ip, int(port))


#Envoi du nom
groupname = "Agar.ia"
manager.send('NME', len(groupname), groupname)


#boucle principale
while True:
    manager.update()
    if manager.game_over == 1:
        print("Bye bye.")
        break

