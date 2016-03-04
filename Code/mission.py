# coding=utf-8                                                                                                                                                                   
from action import Action
from group import Group
#todo utilitaires
from mission_type import MissionType

class Mission:
    def __init__(self, actions=[]):  #Actions is an array of actions
        self.actions=actions
        self.changes
    def calc_mark(self):
        mark=0
        for action in self.actions:
            mark+=action.calc_mark()
        return mark

    def calculateCoup(self, state) #todo
        coups = [0,0]
        for action in self.actions:
            coups[1].append(action.calculateCoup(state))
            coups[0]+=1
        return coups

    def execute(self,state):
        calculatedState = state
        for action in self.actions:
            if action.mission_type == MissionType.attackHuman:
                groupe_en_action= action.assignedGroup
                groupe_vise = action.target_group
                winner = utilitaires.simulateBattle(groupe_en_action,groupe_vise)
                calculatedState.groupes.remove(action.assignedGroup)
                calculatedState.groupes.remove(action.target_group)
                calculatedState.groupes.append(winner)
            if action.mission_type == MissionType.attackEnemy:
                groupe_en_action= action.assignedGroup
                groupe_vise = action.target_group
                winner = utilitaires.simulateBattle(groupe_en_action,groupe_vise) #todo position differente ?
                calculatedState.groupes.remove(action.assignedGroup)
                calculatedState.groupes.remove(action.target_group)
                calculatedState.groupes.append(winner)
            if action.mission_type == MissionType.merge :
                nouveau_groupe = Group(int((action.assignedGroup.x+action.target_group.x)/2),int((action.assignedGroup.x+action.target_group.x)/2),action.target_group.eff+action.assignedGroup.eff,action.assignedGroup.species)
                calculatedState.groupes.remove(action.assignedGroup)
                calculatedState.groupes.remove(action.target_group)
                calculatedState.groupes.append(nouveau_groupe)
            if action.mission_type == MissionType.run :
                groupe_en_action= action.assignedGroup
                groupe_ennemi = action.target_group
                groupe_en_action.x= utilitaires.bordLePlusProche(groupe_en_action,groupe_ennemi)[0],utilitaires.bordLePlusProche(groupe_en_action)[1]
                groupe_en_action.y=
                calculatedState.groupes.remove(action.assignedGroup)
                calculatedState.groupes.remove(action.target_group)
                calculatedState.groupes.append(groupe_en_action)
                calculatedState.groupes.append(groupe_ennemi)

        return calculatedState
