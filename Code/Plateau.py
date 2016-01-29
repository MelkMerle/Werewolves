import Groupe

class PlateauDeJeu :
    def __init__(self):
        self.groupes = Groupe()[]

    def getGroup(self, x, y):
        for groupe in self.groupes:
            if groupe.x=x && groupe.y=y:
                return groupe
        print("Aucun groupe n'a été trouvé par la méthode getGroup")
        return None

    def addGroup(self,x,y):
        self.groupes.append(Groupe(x,y))

    def getHumans(self):

    def getSpecies(self, species):
