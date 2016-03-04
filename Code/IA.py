
from Plateau import PlateauDeJeu
from species import Species
from action import Action
from group import Group
from mission_type import MissionType
from missions_generator import enumerate_possible_missions

import time


class Intelligence():

    def __init__(self):
                                #selon l'interface desiree par l'IA
        self.startTime = time.time()
        self.maxValue =10
        self.mySpecie = Species.human

    def timeleft(self):
        return (5*60)-(time.time() - self.startTime)

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

        if (self.mySpecie == Species.werewolf):
            heuristics = wwNumber - vpNumber
        else:
            heuristics = vpNumber - wwNumber
        return heuristics

    def CalulateNextState(self,mission, state):
        #here we calculate the nextstate, considering a specific mission set
        nextState=mission.execute(state)
        return nextState


     #Principal function, returning the best possible mission set
    def chooseMission(self, state, specie):
        allmission = []
        for mission in enumerate_possible_missions(state, self.mySpecie):
            missiontotest = [self.CalulateNextState(mission, state), 0]
            missiontotest[1] = self.minmax(missiontotest[0], self.mySpecie.invert(), 1)
            allmission.append(missiontotest)
        if specie != self.mySpecie:
            return allmission.sort(key=lambda x: int(x[1]))[0][0].calculateCoup(state)
        else:
            return allmission.sort(key=lambda x: int(x[1]))[len(allmission)][0].calculateCoup(state)

    #Here state is the groups in the possible state, it totally define the game (!!not the real groups though)
    #specie=1 for vampire if its me, 0 for werewolves (just to use ! , I am that lazy)

    def minmax(self, state, specie, recursiveValue):
        allmission=[]
        for mission in enumerate_possible_missions(state, self.mySpecie):
            missiontotest = [self.CalulateNextSate(mission, state), 0]
            if recursiveValue > self.maxValue:
                missiontotest[1] = self.calculateHeuristics(missiontotest[0], specie)
            else:
                missiontotest[1] = self.minmax(missiontotest[0], specie.invert(), recursiveValue+1)
            allmission.append(missiontotest)
        if specie != self.mySpecie:
            return allmission.sort(key=lambda x: int(x[1]))[0][1]
        else:
            return allmission.sort(key=lambda x: int(x[1]))[len(allmission)][1]



