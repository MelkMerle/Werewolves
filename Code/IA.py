from species import Species
import time


class Intelligence ():

    def __init__(self):
                                #selon l'interface desiree par l'IA
        self.startTime = time.time()
        self.maxValue =10
        self.mySpecie = Species.human

    def timeleft(self):
        return (5*60)-(time.time() - self.startTime)

    def calculateHeuristics(self, state, specie):
        # here we do so mathematics voodoo
        heuristics=0
        return heuristics

    def enumeratePossibleMissions(self,state):
        #here we do the possibility elaging, basically, returning an array of mission
        missionArray=self.generate(state)
        sortedMissionArray=[]
        for mission in missionArray:
            sortedMissionArray.append([mission,mission.calc_mark()])
        sortedMissionArray.sort(key=lambda x: int(x[1]))
        return sortedMissionArray[-5:]

    def generate(self,state):
        return


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











