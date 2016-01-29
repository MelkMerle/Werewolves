# coding=utf-8

from species import Species


class Group:

    def __init__(self, x=0, y=0, eff=0, species=Species.human):
        self.x = x
        self.y = y
        self.eff = eff
        self.species = species
        # self.mission = ?? todo

    # def __del__(self):
    # todo

    def __str__(self):
        return "Group of {} {}, en ({},{})".format(self.eff, self.species, self.x, self.y)