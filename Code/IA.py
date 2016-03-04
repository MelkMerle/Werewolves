
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
        groups_ennemy = state.getMembers(self.mySpecie.inverse())
        actionsTotal = []
        lenGroupMe = groupMe.eff
        actionsSimplePerGroup = []
        actionsSplitPerGroup = []
        nMax = int(lenGroupMe/2)
        doublets = []
        # actions sans split
        for groupHuman in groupsHuman:
            action = Action(MissionType.attackHuman, groupHuman, groupMe)
            actionsSimplePerGroup.append(action)
        for group_ennemy in groups_ennemy:
            action = Action(MissionType.attackEnemy, group_ennemy, groupMe)
            actionsSimplePerGroup.append(action)

        # actions avec splits
        for i in range(1, nMax+1):
            doublets.append([i, lenGroupMe-i])
        groups_targets = groupsHuman + groups_ennemy
        for doublet in doublets:
            group1 = Group(groupMe.x, groupMe.y, doublet[0], self.mySpecie)
            group2 = Group(groupMe.x, groupMe.y, doublet[1], self.mySpecie)
            for target_group_1 in groups_targets:
                mission_type_1 = self.mySpecie.determine_mission_type(target_group_1.species)
                for target_group_2 in groups_targets:
                    mission_type_2 = self.mySpecie.determine_mission_type(target_group_2.species)
                    if target_group_1 != target_group_2:
                        action1 = Action(mission_type_1, target_group_1, group1)
                        action2 = Action(mission_type_2, target_group_2, group2)
                        actionsSplitPerGroup.append([action1, action2])
        actionsTotal.append(actionsSimplePerGroup)
        actionsTotal.append(actionsSplitPerGroup)
        return actionsTotal

    def enumeratePossibleMissions(self,state):
        #here we do the possibility elaging, basically, returning an array of mission
        missionArray=[]
        groupsHuman = state.getMembers(Species.human)
        groupsMe = state.getMembers(self.mySpecie)
        for groupMe in groupsMe:
            possibleActions = self.enumeratePossibleActions(state, groupMe)
            rateSimple = 0
            rateSplit = 0
            actionSimple = None
            actionSplit = None

            for action in possibleActions[0]:
                rate = action.calc_mark()
                if rate > rateSimple:
                    actionSimple = action
                    rateSimple = rate

            for actions in possibleActions[1]:
                rate = actions[0].calc_mark() + actions[1].calc_mark()
                if rate > rateSplit:
                    actionSplit = actions
                    rateSplit = rate

            if rateSplit > rateSimple:
                missionArray.append(actionSplit[0])
                missionArray.append(actionSplit[1])
            else:
                missionArray.append(actionSimple)
        return missionArray

        """sortedMissionArray=[]
        for mission in missionArray:
            sortedMissionArray.append([mission,mission.calc_mark()])
        sortedMissionArray.sort(key=lambda x: int(x[1]))
        return sortedMissionArray[-5:]"""

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



