# coding=utf-8
from group import Group


class PlateauDeJeu:

    def __init__(self, width=0, height=0):
        self.groupes = []
        self.width=width
        self.height=height

    def getGroup(self, x, y):
        for groupe in self.groupes:
            if (groupe.x==x and groupe.y==y):
                return groupe
        print 'Aucun groupe trouve aux coordonnees (x,y) suivantes :', x, y
        return None

    def addGroup(self,x, y, effectif, espece):
        nouveau = Group(x, y, effectif, espece)
        return self.addThisGroup(nouveau)

    def addThisGroup(self, group):
        self.groupes.append(group)
        return group

    def getMembers(self, espece):
        members = []
        for group in self.groupes:
            if group.species == espece:
                members.append(group)
        return members

    #quelle est l'idée de cette fonction ?
    # def MoveMembers(self,x, y, xsec,ysec, numtomove):
    #     members = self.getGroup(self,x,y)
    #     if(members != none):





