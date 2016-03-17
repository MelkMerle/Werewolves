# coding=utf-8                                                                                                                                                                   
from action_type import ActionType
from group import Group
from species import Species
import math
import random

def getVector(fromGroup, toGroup):
    distance = [toGroup.x-fromGroup.x,toGroup.y-fromGroup.y]
    vector= [int(distance[0]>0),int(distance[1] >0)]
    return vector

def getDistance(fromGroup, toGroup):
    distance = max(abs(toGroup.x - fromGroup.x), abs(toGroup.y - fromGroup.y) ) #distance de thcebytchev
    return distance

def distance(pos1, pos2):
    return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)

def mergeGroups (group1,group2):
    nouveau_groupe = Group(int((group1.x+group2.x)/2),int((group1.y+group2.y)/2),group1.eff+group2.eff,group1.species)
    return nouveau_groupe

def simulateBattle(groupAtt,groupDef):

    # attaque d'un groupe d'humain avec suffisamment de monde
    if groupDef.species == Species.human and groupAtt.eff >= groupDef.eff:
        group_return = Group(groupDef.x, groupDef.y, groupDef.eff + groupAtt.eff, groupAtt.species)
        return group_return

    # attaque d'un groupe d'ennemis avec sufisamment de monde
    elif groupAtt.eff >= (1.5*groupDef.eff):
        group_return = Group(groupDef.x, groupDef.y, groupDef.eff+groupAtt.eff, groupAtt.species)
        return group_return

   #start a random battle
    winningprob=0
    if groupAtt.eff == groupDef.eff:
        winningprob = 0.5
    if groupAtt.eff < groupDef.eff:
        winningprob = groupAtt.eff/(2*groupDef.eff)
    if groupAtt.eff > groupDef.eff:
        winningprob = groupAtt.eff/groupDef.eff-0.5
    
    if winningprob ==0.5:
        winningprob-=random.random()/100

    if winningprob>0.5:
        eff1=winningprob*groupAtt.eff
        if(groupDef.species=='human'):
            eff1+=winningprob*groupDef.eff
        eff1=int(round(eff1))
        group_return = Group(groupDef.x, groupDef.y, eff1, groupAtt.species)
        return group_return

    else:
        eff2=(1-winningprob)*groupDef.eff
        eff2=int(round(eff2))
        group_return = Group(groupDef.x, groupDef.y, eff2, groupDef.species)
        return group_return

def simulateAttackAction (action, state):
    if action.action_type == ActionType.attackHuman:
            distance = getDistance(action.assignedGroup,action.target_group)
            groupe_max = Group(0,0,0,action.assignedGroup.species.inverse()) #on initialise un groupe max de base, a 0
            for group in state.groupes:
                if group.species == action.assignedGroup.species.inverse() \
                        and getDistance(group,action.target_group) < distance \
                        and group.eff >= action.target_group.eff \
                        and group.eff>groupe_max.eff: #on cherche les groupes ennemis plus proches que nous de la cible, plus nombreux que la cible, et on garde le plus gros d'entre eux
                    groupe_max=group

            enemy_winner = simulateBattle(groupe_max,action.target_group) # on simule une bataille entre ce groupe_max (cad le groupe d'enemis plus proche que nous, ou, à défaut, un groupe fictif vide, qui perdra forcément la bataille)
            return simulateBattle(action.assignedGroup,enemy_winner) # et on simule une bataille entre nous et le gagnant de la première bataille

    elif action.action_type == ActionType.attackEnemy:
            distance = getDistance(action.assignedGroup,action.target_group)
            groupe_max = Group(0,0,0,Species.human) #on initialise un groupe max de base, a 0
            for group in state.groupes:
                if group.species == Species.human \
                        and getDistance(group,action.target_group) < distance \
                        and group.eff <= action.target_group.eff \
                        and group.eff>groupe_max.eff: #on cherche les groupes d'humains plus proches que nous de la cible ennemie, moins nombreuse que la cible, et on garde le plus gros d'entre eux
                    groupe_max=group

            enemy_winner = simulateBattle(groupe_max,action.target_group) # on simule une bataille entre ce groupe_max (cad le groupe d'humains plus proche que nous, ou, à défaut, un groupe fictif vide, qui perdra forcément la bataille)
            return simulateBattle(action.assignedGroup,enemy_winner) # et on simule une bataille entre nous et le gagnant de la première bataille
    else :
        print ("Warning ! simulateAttackAction s'execute sur une action de type autre qu'attackHuman ou attackEnemy")
        return Group()