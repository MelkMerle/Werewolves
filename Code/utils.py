# coding=utf-8                                                                                                                                                                   
from group import Group


def getVector(fromGroup, toGroup):
    distance = [toGroup.x - fromGroup.x, toGroup.y - fromGroup.y]
    norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
    vector= [int(round(distance[0] / norm)),int(round(distance[1] / norm))]
    return vector

def getDistance(fromGroup, toGroup):
    distance = [toGroup.x - fromGroup.x, toGroup.y - fromGroup.y]
    norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
    return norm

def simulateBattle(groupAtt,groupDef):
    if groupDef.species == 'human' and groupAtt.eff>groupDef.eff:
        groupeReturn=groupDef
        groupeReturn.species=groupeAtt.species
        groupeReturn.eff+=groupeDef.e
        return groupeReturn
    elif groupAtt.eff>(1.5*groupDef.eff):
        groupeReturn=groupDef
        groupeReturn.species=groupeAtt.species
        groupeReturn.eff= groupeAtt.eff
        return groupeReturn

   #start a random battle
    winningprob=0
    if groupAtt.eff==groupeDef.eff:
        winningprob=0.5
    if groupAtt.eff<groupDef.eff:
        winningprob=groupAtt.eff/(2*groupDef.eff)
    if groupAtt.eff>eff2:
        winningprob= groupAtt.eff/groupDef.eff-0.5
    
    if winningprob ==0.5:
        winningprob+=random.random()/100 

    if winningprob>0.5:
        eff1=winningprob*groupAtt.eff
        if(grouDef.species=='human'):
            eff1+=winningprob*groupDef.eff
        eff1=int(round(eff1))
        groupeReturn=groupeDef
        groupeReturn.species=groupAtt.species
        groupeReturn.eff=eff1
        return groupeReturn

    else:
        eff2=(1-winningprob)*groupDef.eff
        eff1=int(round(eff1))                                                                                                                                       
        groupeReturn=groupeDef
        groupeReturn.eff=eff2
        return groupeReturn
