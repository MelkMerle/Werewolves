# coding=utf-8
from group import Group


class PlateauDeJeu:

    def __init__(self,width,height):
        self.groupes = []
        self.width=width
        self.height=height
    
    def getGroup(self, x, y):
        for groupe in self.groupes:
            if (groupe.x==x & groupe.y==y):
                return groupe
        print("Aucun groupe n'a été trouvé par la méthode getGroup")
        return None

    def addGroup(self,x, y, effectif, espece):
        nouveau = Group(x, y, effectif, espece)
        self.groupes.append(nouveau)
        return nouveau

    def getMembers(self, espece):
        members = []
        for group in self.groupes:
            if group.species == espece:
                members.append(group)
        return members

    def MoveMembers(self,x, y, xsec,ysec, numtomove)
        members=getGroup(self,x,y)
        if(members !=none)





