# coding=utf-8                                                                                                                                                                   
from action import Action
from group import Group
from mission_type import MissionType

class Mission:
    def __init__(self, actions=[]):  #Actions is an array of actions
        self.actions=actions

    def calc_mark(self):
        mark=0
        for action in self.actions:
            mark+=action.calc_mark()
        return mark

    # def calculateCoup(self):
    #     coups[0,0]
    #     for action in self.actions:
    #         coups[1].append(action.calculateCoup())
    #         coups[0]+=1
    #     return coups


