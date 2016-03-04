# coding=utf-8

from enum import Enum


class Species(Enum):
    human = 'human'
    werewolf = 'werewolf'
    vampire = 'vampire'

    def inverse(self):
        if self.value == 'vampire':
            return Species.werewolf
        if self.value == 'werewolf':
            return Species.vampire
        return Species.human
