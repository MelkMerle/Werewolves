
from species import Species
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
    def chooseMission(self, state):
        possibleBranches = []
        missionlist = enumerate_possible_missions(state, self.mySpecie)
        for mission in missionlist:
            assessedMission = [mission, 0]
            assessedMission[1] = self.alphabeta(self.CalulateNextState(mission, state), self.mySpecie.inverse(), 1,-100000, +100000)
            possibleBranches.append(assessedMission)
        coupFinal = possibleBranches.sort(key=lambda x: int(x[1]))[len(possibleBranches)][0].calculateCoup(state)
        return coupFinal

    #Here state is the groups in the possible state, it totally define the game (!!not the real groups though)
    #specie=1 for vampire if its me, 0 for werewolves (just to use ! , I am that lazy)
    def alphabeta(self, state, specie, recursiveValue, alpha, beta):
        if recursiveValue > self.maxValue:
            return  self.calculateHeuristics(state)
        if specie== self.mySpecie:
            missionList = enumerate_possible_missions(state, specie)
            print("alpha liste", missionList)
            for mission in missionList:
                alpha=max(alpha,self.alphabeta(mission.execute(state), specie.inverse(), recursiveValue+1,alpha, beta))
                if alpha > beta:
                    return beta
            return alpha
        else:
            missionList = enumerate_possible_missions(state, specie)
            print("beta liste ", missionList)
            for mission in missionList:
                beta=min(beta,self.alphabeta(mission.execute(state), specie.inverse(), recursiveValue+1,alpha, beta))
                if alpha > beta :
                    return alpha
            return beta

        



