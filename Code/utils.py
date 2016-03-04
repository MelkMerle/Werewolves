# coding=utf-8                                                                                                                                                                   
from group import Group
import math


def getVector(fromGroup, toGroup):
    distance = [toGroup.x - fromGroup.x, toGroup.y - fromGroup.y]
    norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
    vector= [int(round(distance[0] / norm)),int(round(distance[1] / norm))]
    return vector

def getDistance(fromGroup, toGroup):
    distance = [toGroup.x - fromGroup.x, toGroup.y - fromGroup.y]
    norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
    return norm


def mergeGroups (group1,group2):
    nouveau_groupe = Group(int((group1.x+group2.x)/2),int((group1.y+group2.y)/2),group1.eff+group2.eff,group1.species)
    return nouveau_groupe

def simulateBattle(groupAtt,groupDef):
    if groupDef.species == 'human' and groupAtt.eff>groupDef.eff:
        groupeReturn=groupDef
        groupeReturn.species=groupAtt.species
        groupeReturn.eff+=groupAtt.eff
        return groupeReturn
    elif groupAtt.eff>(1.5*groupDef.eff):
        groupeReturn=groupDef
        groupeReturn.species=groupAtt.species
        groupeReturn.eff= groupAtt.eff
        return groupeReturn

   #start a random battle
    winningprob=0
    if groupAtt.eff==groupDef.eff:
        winningprob=0.5
    if groupAtt.eff<groupDef.eff:
        winningprob=groupAtt.eff/(2*groupDef.eff)
    if groupAtt.eff>groupDef.eff:
        winningprob= groupAtt.eff/groupDef.eff-0.5
    
    if winningprob ==0.5:
        winningprob+=math.random()/100

    if winningprob>0.5:
        eff1=winningprob*groupAtt.eff
        if(groupDef.species=='human'):
            eff1+=winningprob*groupDef.eff
        eff1=int(round(eff1))
        groupeReturn=groupDef
        groupeReturn.species=groupAtt.species
        groupeReturn.eff=eff1
        return groupeReturn

    else:
        eff2=(1-winningprob)*groupDef.eff
        eff2=int(round(eff2))                                                                                                                                       
        groupeReturn=groupDef
        groupeReturn.eff=eff2
        return groupeReturn
