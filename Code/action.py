# coding=utf-8

from group import Group
from mission_type import MissionType


class Action:

    def __init__(self, mission_type, target_group, assigned_group):
        self.mission_type = mission_type
        self.target_group = target_group
        self.assignedGroup = assigned_group

        self.secure_effective = target_group.eff
        self.possibleGain = 0
        self.possibleLoss = 0
        self.possibleEnemyLoss = 0
        self.possibleEnemyGain = 0

        self.mark = 0

    def calc_mark(self):
        if self.mission_type == MissionType.attackHuman:
            if self.assignedGroup.eff > self.secure_effective:
                self.possibleGain = self.target_group.eff
                self.possibleLoss = 0 #todo
                self.possibleEnemyLoss = 0  #todo
                self.possibleEnemyGain = 0 #todo
        elif self.mission_type == MissionType.attackEnemy: #todo
            return
        elif self.mission_type == MissionType.run:  #todo
            self.possibleGain = 0 #todo
        mark= (self.possibleGain+self.possibleEnemyLoss-self.possibleEnemyGain-self.possibleLoss)
        return mark

    def __str__(self):
        return "Group of {} {}, en ({},{})".format(self.eff, self.species.value, self.x, self.y)


    def calculateCoup(self, state):
        #dependant on mission type
        #test if below limit lines before sending!!

        if self.mission_type ==MissionType.attackHuman:
            #find closest human group
            grouptoAttack=self.target_group
            vector=utils.getVector(self.assignedGroup,grouptoAttack)
                #here if no split
            return [self.assignedGroup.x, self.assignedGroup.y, self.assignedGroup.eff, self.assignedGroup.x+vector[0], self.assignedGroup.y+vector[1]]
        
        if self.mission_type == MissionType.attackEnemy:
            #find closest ennemy group
            grouptoAttack=self.target_group
            vector=utils.getVector(self.assignedGroup,grouptoAttack)
                #here if no split
            return [self.assignedGroup.x, self.assignedGroup.y, self.assignedGroup.eff, self.assignedGroup.x+vector[0],self.assignedGroup.y+vector[1]]
 
        if self.mission_type == MissionType.run:
            #find closest ennemy group
            grouptoRunfrom=self.target_group
            vector=utils.getVector(self.assignedGroup,grouptoRunfrom)
                #here if no split
            if state.width<(self.assignedGroup.x-vector[0]):
                vector[0]+=1
            elif (self.assignedGroup.x-vector[0]) <0:
                vector[0]-=1 
            if state.height<(self.assignedGroup.y-vector[1]):
                vector[1]-=1 
            elif (self.assignedGroup.y-vector[1]) <0:
                vector[1]+=1

            return [self.assignedGroup.x, self.assignedGroup.y, self.assignedGroup.eff, self.assignedGroup.x-vector[0], self.assignedGroup.y-vector[1]]




    
