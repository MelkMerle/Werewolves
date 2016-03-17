
import copy
from species import Species
from missions_generator import enumerate_possible_missions

import time


class Intelligence():

    def __init__(self, maxTime=0.8, recursiveDepth=4, branchFactor=3, max_split_rate=3):
                                #selon l'interface desiree par l'IA
        self.startTime = time.time()
        self.maxTime=maxTime
        self.mySpecie = Species.human
        self.maxRecursiveValue=recursiveDepth
        self.branchFactor = branchFactor
        self.max_split_rate = max_split_rate
    def timeleft(self):
        return (5*60)-(time.time() - self.startTime)

    def generate(self,state):

        return


    def calculateHeuristics(self,state):
        # here we do so mathematics voodoo
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
        self.startTime = time.time()
        possibleBranches = []
        missionlist = enumerate_possible_missions(state, self.mySpecie, self.branchFactor, self.max_split_rate)
        #print("alpha 1 ", missionlist)
        for mission in missionlist:
            assessedMission = [mission, 0]
            assessedMission[1] = self.alphabeta(self.CalulateNextState(mission, state),1, self.mySpecie.inverse(),-100000, +100000) #appel recursif du alphabeta
            possibleBranches.append(assessedMission)
        print(possibleBranches)
        coupFinal = sorted(possibleBranches, key=lambda x: (x[1]))[-1][0].calculateCoup(state)
        return coupFinal

    #Here state is the groups in the possible state, it totally define the game (!!not the real groups though)
    #specie=1 for vampire if its me, 0 for werewolves (just to use ! , I am that lazy)
    def alphabeta(self, state, recursiveValue, specie,  alpha, beta):
        if (self.maxRecursiveValue <= recursiveValue) or (state.getMembers(specie)==[]) or (state.getMembers(specie.inverse())==[]) or ((time.time()-self.startTime)>self.maxTime) :
            print((time.time()-self.startTime))
            print(recursiveValue)
            return  self.calculateHeuristics(state)
        if specie == self.mySpecie:
            missionList = enumerate_possible_missions(state, specie, self.branchFactor,self.max_split_rate)
            #print("alpha liste", missionList)
            for mission in missionList:
                alpha = max(alpha, self.alphabeta(mission.execute(state),recursiveValue+1 , specie.inverse(),alpha, beta))
                if alpha > beta:
                    return beta
            return alpha
        else:
            missionList = enumerate_possible_missions(state, specie, self.branchFactor,self.max_split_rate)
            #print("beta liste ", missionList)
            for mission in missionList:
                beta=min(beta,self.alphabeta(mission.execute(state),recursiveValue+1, specie.inverse(),alpha, beta))
                if alpha > beta :
                    return alpha
            return beta

        



