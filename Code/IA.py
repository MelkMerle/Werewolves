from Plateau import PlateauDeJeu
from species import Species
import time


class Intelligence (PlateauDeJeu):

    def __init__(self,plateau):
        self.mySpecie = 0
        self.state = plateau    #le plateau (liste des groupes, lignes, colonnes), pourra eventuellement etre modifie
                                #selon l'interface desiree par l'IA
        self.startTime = time.time()
        self.maxValue =10
        
    
    def timeleft(self):
        return (5*60)-(time.time() - self.startTime)

def calculateHeuristics(state, myspecie):
    # here we do so mathematics voodoo
    heuristics=0
    wwGroups=state.getMembers(Species.werewolf)
    vpGroups=state.getMembers(Species.vampire)
    wwNumber=0
    vpNumber=0
    for g in wwGroups:
        wwNumber=wwNumber + g.eff
    for g in vpGroups:
        vpNumber=vpNumber + g.eff

    if (myspecie==Species.werewolf):
        heuristics=wwNumber - vpNumber
    else:
        heuristics=vpNumber - wwNumber
    return heuristics


    def enumeratePossibleMissions(self, state):
        #here we do the possibility elaging, basically, returning an array of mission
        missionAssigement=[1]
        return missionAssigement
    
 def CalulateNextSate(self, mission, state):
        #here we calculate the nextstate, considering a specific mission set
        if(mission==1):
            #look for humans
            foes= state.getMembers(state, 2)
            #look where I am
            me=state.getMembers(state,self.mySpecie = 0)
            #now move towards closest human group
            
        
            
        return nextState

#Principal function, returning the best possible mission set
def Choose(self, state,specie):
        allmission=[]
        for mission in enumeratePossibleMissions(state):
            missiontotest=[CalulateNextSate(mission, state),0]
            missiontotest[1]=minmax(missiontotest[0],!specie,1)
            allmission.append(missiontotest)
        if(specie!=self.mySpecie):
            return allmission.sort(key=lambda x: int(x[1]))[0][0]
        else:
            return allmission.sort(key=lambda x: int(x[1]))[len(allmission)][0]


    


    #Here state is the groups in the possible state, it totally define the game (!!not the real groups though)
    #specie=1 for vampire if its me, 0 for werewolves (just to use ! , I am that lazy)

def minmax(self, state, specie, recursiveValue):
        allmission=[]
        for mission in enumeratePossibleMissions(state):
            missiontotest=[CalulateNextSate(mission, state),0]
            if(recursiveValue>self.maxValue):
                missiontotest[1]=calculateHeuristics( missiontotest[0],specie)
            else:
                missiontotest[1]=minmax(missiontotest[0],!specie,recursiveValue+1)
            allmission.append(missiontotest)
        if(specie!=self.mySpecie):
            return allmission.sort(key=lambda x: int(x[1]))[0][1]
        else:
            return allmission.sort(key=lambda x: int(x[1]))[len(allmission)][1]
        









