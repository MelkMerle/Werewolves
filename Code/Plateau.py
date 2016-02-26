# coding=utf-8
from group import Group


class PlateauDeJeu:

    def __init__(self,width=0,height=0):
        self.groupes = []
        self.width=width
        self.height=height
        self.maMaison = [0,0]
    
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

    def delGroup(self, x,y):
        groupe = self.getGroup(x,y)
        groupe._del_()

    def getMembers(self, espece):
        members = []
        for group in self.groupes:
            if group.species == espece:
                members.append(group)
        return members

    # def MoveMembers(self,x, y, xsec,ysec, numtomove):
    #     members = self.getGroup(self,x,y)
    #     if(members != none):





