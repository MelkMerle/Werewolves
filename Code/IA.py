
from Plateau import PlateauDeJeu
from species import Species
from action import Action
from group import Group
from mission_type import MissionType
import time


class Intelligence ():

    def __init__(self):
                                #selon l'interface desiree par l'IA
        self.startTime = time.time()
        self.maxValue =10
        self.mySpecie = Species.human

    def timeleft(self):
        return (5*60)-(time.time() - self.startTime)


    def enumeratePossibleActions(self, state, groupMe):
        groupsHuman = state.getMembers(Species.human)
        actionsSimple = []
        actionsSplit = []
        actionsTotal = []
        lenGroupMe = len(groupMe)
        actionsSimplePerGroup = []
        actionsSplitPerGroup = []
        nMax = int(lenGroupMe/2)
        doublets = []
        # actions sans split
        for groupHuman in groupsHuman:
            action = Action(groupMe, groupHuman, MissionType.attackHuman)
            actionsSimplePerGroup.append(action)
        actionsSimple.append(actionsSimplePerGroup)

        # actions avec splits
        for i in range(0, nMax+1):
            doublets.append([i, lenGroupMe-i])
        for doublet in doublets:
            group1 = Group(groupMe.x, groupMe.y, doublet[0], self.mySpecie)
            group2 = Group(groupMe.x, groupMe.y, doublet[1], self.mySpecie)
            for groupHuman in groupsHuman:
                action1 = Action(group1, groupHuman, MissionType.attackHuman)
                action2 = Action(group2, groupHuman, MissionType.attackHuman)
                actionsSplitPerGroup.append([action1, action2])
        actionsSplit.append(actionsSplitPerGroup)
        actionsTotal.append(actionsSimple)
        actionsTotal.append(actionsSplit)
        return actionsTotal

    def enumeratePossibleMissions(self,state):
        #here we do the possibility elaging, basically, returning an array of mission
        missionArray=[]
        groupsHuman = state.getMembers(Species.human)
        groupsMe = state.getMembers(self.mySpecie)

        sortedMissionArray=[]
        for mission in missionArray:
            sortedMissionArray.append([mission,mission.calc_mark()])
        sortedMissionArray.sort(key=lambda x: int(x[1]))
        return sortedMissionArray[-5:]

    def generate(self,state):

        return


    def calculateHeuristics(self,state):
        # here we do so mathematics voodoo
        heuristics=0
        wwGroups = state.getMembers(Species.werewolf)
        vpGroups = state.getMembers(Species.vampire)
        wwNumber= 0
        vpNumber= 0
        for g in wwGroups:
            wwNumber = wwNumber + g.eff
        for g in vpGroups:
            vpNumber = vpNumber + g.eff

        if (self.mySpecies == Species.werewolf):
            heuristics = wwNumber - vpNumber
        else:
            heuristics = vpNumber - wwNumber
        return heuristics

    def CalulateNextSate(mission, state):
        #here we calculate the nextstate, considering a specific mission set
        nextState=mission.execute(state)
        return nextState


     #Principal function, returning the best possible mission set
    def Choose(self, state, specie):
        allmission=[]
        for mission in self.enumeratePossibleMissions(state):
            missiontotest=[self.CalulateNextSate(mission, state),0]
            missiontotest[1]=self.minmax(missiontotest[0],self.mySpecie.invert(),1)
            allmission.append(missiontotest)
        if(specie!=self.mySpecie):
            return allmission.sort(key=lambda x: int(x[1]))[0][0]
        else:
            return allmission.sort(key=lambda x: int(x[1]))[len(allmission)][0]

    #Here state is the groups in the possible state, it totally define the game (!!not the real groups though)
    #specie=1 for vampire if its me, 0 for werewolves (just to use ! , I am that lazy)

    def minmax(self,state, specie, recursiveValue):
        allmission=[]
        for mission in self.enumeratePossibleMissions(state):
            missiontotest=[self.CalulateNextSate(mission, state),0]
            if(recursiveValue>self.maxValue):
                missiontotest[1] = self.calculateHeuristics( missiontotest[0],specie)
            else:
                missiontotest[1] = self.minmax(missiontotest[0],specie.invert(),recursiveValue+1)
            allmission.append(missiontotest)
        if(specie!=self.mySpecie):
            return allmission.sort(key=lambda x: int(x[1]))[0][1]
        else:
            return allmission.sort(key=lambda x: int(x[1]))[len(allmission)][1]



