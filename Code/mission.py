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
        coupsActions = []
        coupsNombre = 0
        startCases = []
        destCases = []
        for action in self.actions: #todo eviter de se marcher dessus (case de depart = case d'arrivee)
            print(action)
            coup = action.calculateCoup(state)
            print(coup)
            coords_init = [coup[0], coup[1]]
            coords_dest = [coup[3], coup[4]]
            print(startCases)
            startCases.append(coords_init)
            destCases.append(coords_dest)

            coupsActions.append(coup)
            coupsNombre += 1
        coups = [coupsNombre, coupsActions]
        return coups

    def execute(self,state):
        # for action in self.actions :
        #     print(action)

        calculatedState = copy.deepcopy(state)
        for action in self.actions: #on parcourt les actions possibles
            #print "action executee par alphabeta :", action

            # pour les missions de type attackhuman, on simule l'état du plateau quand on l'aura bouffé
            if action.action_type == ActionType.attackHuman:
                winner = utils.simulateBattle(action.assignedGroup,action.target_group)

                #on vérifie juste si il ya un split, car si il y en a il faut effacer le groupe parent et non le "sous-groupe" qui effectue l'action
                if action.parent_group != None:
                    calculatedState.removeGroup(action.parent_group)
                else :
                    calculatedState.removeGroup(action.assignedGroup)

                calculatedState.removeGroup(action.target_group)
                calculatedState.groupes.append(winner)

            # pour les actions de type attack enemy, pareil.
            # todo à améliorer, car si on arrive pas a bouffer l'ennemi, c'est pas une bonne mission (par exemple distance trop grande), il ne faut pas simuler une map comme si on l'avait bouffé mais plutot une map ou il est en triain de run from us
            if action.action_type == ActionType.attackEnemy:
                winner = utils.simulateBattle(action.assignedGroup,action.target_group)

                #on vérifie juste qu'il n'y a pas de split, si il y en a il faut effacer le groupe parent et pas le "sous-groupe" qui effectue l'action
                if action.parent_group != None:
                    calculatedState.removeGroup(action.parent_group)
                else :
                    calculatedState.removeGroup(action.assignedGroup)

                calculatedState.removeGroup(action.target_group)
                calculatedState.groupes.append(winner)

            # pour les merge, on change le palteau comme il faut
            if action.action_type == ActionType.merge :
                nouveau_groupe = utils.mergeGroups(action.assignedGroup,action.target_group)
                calculatedState.removeGroup(action.assignedGroup)
                calculatedState.removeGroup(action.target_group)
                calculatedState.groupes.append(nouveau_groupe)

            # run pas encore implementee
            if action.action_type == ActionType.run :
                groupe_en_action= action.assignedGroup
                groupe_ennemi = action.target_group
                groupe_en_action.x= utils.bordLePlusProche(groupe_en_action,groupe_ennemi)[0] #todo comment simuler le plateau quand on a couru ?
                groupe_en_action.y= utils.bordLePlusProche(groupe_en_action)[1]
                calculatedState.removeGroup(action.assignedGroup)
                calculatedState.removeGroup(action.target_group)
                calculatedState.groupes.append(groupe_en_action)
                calculatedState.groupes.append(groupe_ennemi)

        return calculatedState
