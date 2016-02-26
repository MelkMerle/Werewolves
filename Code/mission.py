# coding=utf-8

from group import Group
from mission_type import MissionType


class Mission:

    def __init__(self, mission_type, target_group):
        self.mission_type = mission_type
        self.target_group = target_group
        self.assignedGroup = None

        self.secure_effective = 0
        self.possibleGain = 0
        self.possibleLoss = 0
        self.possibleEnemyLoss = 0
        self.possibleEnemyGain = 0

        self.mark = 0

    def calc_mark(self):
        if self.mission_type == MissionType.attackHuman:
            self.secure_effective = self.target_group.eff
            self.possibleGain = self.target_group.eff
            self.possibleLoss = 0
            self.possibleEnemyLoss = 0
            self.possibleEnemyGain = 0


    def __str__(self):
        return "Group of {} {}, en ({},{})".format(self.eff, self.species.value, self.x, self.y)



    def execute(self):
        self.evaluateCoup()
        #générer plateau a partir du coup todo

    def evaluateCoup(self):
        # todo
        return 0