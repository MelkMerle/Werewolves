# coding=utf-8                                                                                                                                                                   
from action import Action
from group import Group
import utils
import copy
from action_type import ActionType

class Mission:
    def __init__(self, actions=[Action()]):  # Actions is an array of actions
        self.actions=actions
        #self.changes inutile maintenant
    def calc_mark(self,state):
        mark=0
        for action in self.actions:
            mark+=action.calc_mark(state)
        return mark


    def calculateCoup(self, state):
        coupsActions =[]
        coupsNombre = 0
        for action in self.actions:
            coupsActions.append(action.calculateCoup(state))
            coupsNombre += 1
        coups = [coupsNombre,coupsActions]
        return coups

    def execute(self,state):
        print(self.actions)
        calculatedState = copy.deepcopy(state)
        for action in self.actions: #on parcourt les actions possibles
            if action.action_type == ActionType.attackHuman:
                groupe_en_action = action.assignedGroup
                groupe_vise = action.target_group
                winner = utils.simulateBattle(groupe_en_action,groupe_vise)
                calculatedState.groupes.remove(action.assignedGroup)
                calculatedState.groupes.remove(action.target_group)
                calculatedState.groupes.append(winner)

           # pour les missions de type attackhuman, on simule l'état du plateau quand on l'aura bouffé
            if action.action_type == ActionType.attackEnemy:
                groupe_en_action= action.assignedGroup
                groupe_vise = action.target_group
                winner = utils.simulateBattle(groupe_en_action,groupe_vise) #todo position differente ?
                calculatedState.groupes.remove(action.assignedGroup)
                calculatedState.groupes.remove(action.target_group)
                calculatedState.groupes.append(winner)

            if action.action_type == ActionType.merge :
                nouveau_groupe = utils.mergeGroups(action.assignedGroup,action.target_group)
                calculatedState.groupes.remove(action.assignedGroup)
                calculatedState.groupes.remove(action.target_group)
                calculatedState.groupes.append(nouveau_groupe)

            if action.action_type == ActionType.run :
                groupe_en_action= action.assignedGroup
                groupe_ennemi = action.target_group
                groupe_en_action.x= utils.bordLePlusProche(groupe_en_action,groupe_ennemi)[0] #todo comment simuler le plateau quand on a couru ?
                groupe_en_action.y= utils.bordLePlusProche(groupe_en_action)[1]
                calculatedState.groupes.remove(action.assignedGroup)
                calculatedState.groupes.remove(action.target_group)
                calculatedState.groupes.append(groupe_en_action)
                calculatedState.groupes.append(groupe_ennemi)

        return calculatedState
