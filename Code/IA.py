# coding=utf-8

class Intelligence:
    def __init__(self, plateau):
        self.groups = plateau.groupes
        self.coup = [1,4,3,1,5,4]
        self.lignes = 0
        self.colonnes = 0
        self.maMaison = [0, 0]
    def calculDuCoup(self):
        return 1