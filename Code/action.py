﻿# coding=utf-8

from group import Group
from action_type import ActionType
from species import Species
import utils

class Action:

    def __init__(self, action_type=ActionType.attackHuman, target_group=Group(), assigned_group=Group()):
        self.action_type = action_type
        self.target_group = target_group
        self.assignedGroup = assigned_group
        self.parent_group = None

        self.secure_effective = target_group.eff
        self.possibleGain = 0
        self.possibleLoss = 0
        self.possibleEnemyLoss = 0
        self.possibleEnemyGain = 0

        self.mark = 0

    def calc_mark(self, state): #a ameliorer pour la gestion des ennemis
        if self.assignedGroup.eff==0:
            print("Warning : calc_mark tente d'evaluer les actions d'un groupe vide")
            return 0
        if self.action_type == ActionType.attackHuman:
            distance = utils.getDistance(self.assignedGroup,self.target_group)
            groupe_max = Group(0,0,0,self.assignedGroup.species.inverse()) #on initialise un groupe max de base, a 0
            for group in state.groupes:
                if group.species == self.assignedGroup.species.inverse() \
                        and utils.getDistance(group,self.target_group) < distance \
                        and group.eff >= self.target_group.eff \
                        and group.eff>groupe_max.eff: #on cherche les groupes ennemis plus proches que nous de la cible, plus nombreux que la cible, et on garde le plus gros d'entre eux
                    groupe_max=group

            enemyWinner = utils.simulateBattle(groupe_max,self.target_group) # on simule une bataille entre ce groupe_max (cad le groupe d'enemis plus proche que nous, ou, à défaut, un groupe fictif vide, qui perdra forcément la bataille)
            winnerFinal = utils.simulateBattle(self.assignedGroup,enemyWinner) # et on simule une bataille entre nous et le gagnant de la première bataille
            #et ensuite on traite les differents cas

            if winnerFinal.species==self.assignedGroup.species: #soit on gagne avec certitude la derniere bataille
                self.possibleEnemyGain = -groupe_max.eff
                self.possibleGain = (winnerFinal.eff)-self.assignedGroup.eff

            elif winnerFinal.species == Species.human: # soit les humains remportent et nos deux groupes se sont faits bouffer (on a été cons)
                self.possibleEnemyGain = -groupe_max.eff
                self.possibleGain = -self.assignedGroup.eff

            else:                                       # soit les enemis gagnent et on perd
                self.possibleEnemyGain = (winnerFinal.eff)-groupe_max.eff
                self.possibleGain = -self.assignedGroup.eff


        elif self.action_type == ActionType.attackEnemy:
            distance = utils.getDistance(self.assignedGroup,self.target_group)
            groupe_max = Group(0,0,0,Species.human) #on initialise un groupe max de base, a 0
            for group in state.groupes:
                if group.species == Species.human \
                        and utils.getDistance(group,self.target_group) < distance \
                        and group.eff <= self.target_group.eff \
                        and group.eff>groupe_max.eff: #on cherche les groupes d'humains plus proches que nous de la cible ennemie, moins nombreuse que la cible, et on garde le plus gros d'entre eux
                    groupe_max=group

            enemyWinner = utils.simulateBattle(self.target_group,groupe_max) # on simule une bataille entre ce groupe_max (cad le groupe d'humains plus proche que nous, ou, à défaut, un groupe fictif vide, qui perdra forcément la bataille)
            winnerFinal = utils.simulateBattle(self.assignedGroup,enemyWinner) # et on simule une bataille entre nous et le gagnant de la première bataille

            if winnerFinal.species==self.assignedGroup.species:
                self.possibleGain = (winnerFinal.eff)-self.assignedGroup.eff
                self.possibleEnemyGain = -self.target_group.eff
            else :
                self.possibleGain = -self.assignedGroup.eff
                self.possibleEnemyGain = (winnerFinal.eff-self.target_group.eff)

        elif self.action_type == ActionType.run:  #todo a implementer en cas de plateau vide à la fin si on est plus nombreux que les ennemis
            self.possibleGain = 0
        else :
            print("type d'action non reconnu par calc_mark", self.action_type)
        intuitive_mark = (self.possibleGain-self.possibleEnemyGain)
        #enfin, on divise les notes intuitives par la distance pour prendre en compte des incertitudes
        if intuitive_mark >= 0:
            self.mark = intuitive_mark/float(utils.getDistance(self.assignedGroup,self.target_group)) #todo diviser par distance au carre ?
        else : #mais on garde les notes négatives telles quelles pour leur donner plus de poids negatif
            self.mark = intuitive_mark


    def __str__(self):
        return "{} from {} to {}, note {}".format(self.action_type, self.assignedGroup, self.target_group, self.mark)



    def calculateCoup(self, state):
        #depend du action_type
        if self.action_type ==ActionType.attackHuman or self.action_type == ActionType.attackEnemy:
            vector = utils.getVector(self.assignedGroup,self.target_group)
            return [self.assignedGroup.x, self.assignedGroup.y, self.assignedGroup.eff, self.assignedGroup.x+vector[0], self.assignedGroup.y+vector[1]]

        #run pas encore implemente, malheureusement
        if self.action_type == ActionType.run:
            #find closest ennemy group
            grouptoRunfrom=self.target_group
            vector=utils.getVector(self.assignedGroup,grouptoRunfrom)
            if state.width<(self.assignedGroup.x-vector[0]):
                vector[0]+=1
            elif (self.assignedGroup.x-vector[0]) <0:
                vector[0]-=1 
            if state.height<(self.assignedGroup.y-vector[1]):
                vector[1]-=1 
            elif (self.assignedGroup.y-vector[1]) <0:
                vector[1]+=1
            #todo check qu'on ne sorte pas de la carte

            return [self.assignedGroup.x, self.assignedGroup.y, self.assignedGroup.eff, self.assignedGroup.x-vector[0], self.assignedGroup.y-vector[1]]
