# coding=utf-8

from enum import Enum
from action_type import ActionType

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

    def determine_action_type(self, target_species):
        if target_species == self:
            return ActionType.merge
        if target_species == self.inverse():
            return ActionType.attackEnemy
        if target_species == Species.human:
            return ActionType.attackHuman
        else :
            print("determine mission type encountered problem car l'espece visee etait", target_species)
