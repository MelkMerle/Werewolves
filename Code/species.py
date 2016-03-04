# coding=utf-8

from enum import Enum
from mission_type import MissionType

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

    def determine_mission_type(self, target_species):
        if target_species.value == self.value:
            return MissionType.merge
        if target_species.value == self.inverse().value:
            return MissionType.attackEnemy
        if target_species.value == Species.human.value:
            return MissionType.attackHuman

