# coding=utf-8
from species import Species
from missions_generator import enumerate_possible_missions

import time


class Intelligence():

    def __init__(self, maxTime=0.8, recursiveDepth=4, branchFactor=3, max_split_rate=3):
                                # paramètres à régler par experimentation (depend de la map aussi)
        self.startTime = time.time()
        self.maxTime = maxTime
        self.mySpecie = Species.human
        self.maxRecursiveValue=recursiveDepth
        self.branchFactor = branchFactor
        self.max_split_rate = max_split_rate

    def timeleft(self):
        return (5*60)-(time.time() - self.startTime)



    def calculateHeuristics(self,state):
        #heuristique simpliste au possible, pour qu'elle ne soit pas trop lourde à calculer
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

     #Fonction principale, qui retourne le meilleur coup possible
    def chooseMission(self, state):
        self.startTime = time.time() # on lance un timer au debut du tour, pour eviter le timeout

        possibleBranches = []
        missionlist = enumerate_possible_missions(state, self.mySpecie, self.branchFactor, self.max_split_rate)
        for mission in missionlist:
            assessedMission = [mission, 0]
            assessedMission[1] = self.alphabeta(mission.execute(state),1, self.mySpecie.inverse(),-100000, +100000) #appel recursif du alphabeta
            possibleBranches.append(assessedMission)
        #possibleBranches est une liste de tuples : <mission possible, note alphabeta de cette mission>, une mission etant constituée d'une liste d'actions pour chaque groupe
        coupFinal = sorted(possibleBranches, key=lambda x: (x[1]))[-1][0].calculateCoup(state) #on calcule le coup de la meilleure mission
        return coupFinal

    #Here state is the groups in the possible state, it totally defines the game (!!not the real groups though)

    def alphabeta(self, state, recursiveValue, specie,  alpha, beta):
        #condition d'arret
        if (self.maxRecursiveValue <= recursiveValue) or (state.getMembers(specie)==[]) or (state.getMembers(specie.inverse())==[]) or ((time.time()-self.startTime)>self.maxTime) :
            return  self.calculateHeuristics(state)
        #branche alpha
        if specie == self.mySpecie:
            missionList = enumerate_possible_missions(state, specie, self.branchFactor,self.max_split_rate)
            for mission in missionList:
                alpha = max(alpha, self.alphabeta(mission.execute(state),recursiveValue+1 , specie.inverse(),alpha, beta))
                if alpha > beta:
                    return beta
            return alpha
        #branche beta
        else:
            missionList = enumerate_possible_missions(state, specie, self.branchFactor,self.max_split_rate)
            for mission in missionList:
                beta=min(beta,self.alphabeta(mission.execute(state),recursiveValue+1, specie.inverse(),alpha, beta))
                if alpha > beta :
                    return alpha
            return beta

        



