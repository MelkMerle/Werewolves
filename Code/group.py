# coding=utf-8

from species import Species

class Group:

    def __init__(self, x=0, y=0, eff=0, species=Species.human):
        self.x = x
        self.y = y
        self.eff = eff
        self.species = species

    def __str__(self):
        return "groupe de {}{} en ({},{})".format(self.eff, self.species.value, self.x, self.y)
