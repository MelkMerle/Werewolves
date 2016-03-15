# coding=utf-8

from group import Group
from action_type import ActionType
from species import Species
import utils

class Action:

    def __init__(self, action_type=ActionType.attackHuman, target_group=Group(), assigned_group=Group()):
        self.action_type = action_type
        self.target_group = target_group
        self.assignedGroup = assigned_group
        self.parent_group = None

        self.secure_effective = target_group.eff
        self.possibleGain = 0
        self.possibleLoss = 0
        self.possibleEnemyLoss = 0
        self.possibleEnemyGain = 0

        self.mark = 0

    def calc_mark(self, state): #a ameliorer pour la gestion des ennemis
        if self.assignedGroup.eff==0:
            print("Warning : calc_mark tente d'evaluer les actions d'un groupe vide")
            return 0
        if self.action_type == ActionType.attackHuman:
            distance = utils.getDistance(self.assignedGroup,self.target_group)
            groupe_max = Group(0,0,0,self.assignedGroup.species.inverse()) #on initialise un groupe max de base, a 0
            for group in state.groupes:
                if group.species == self.assignedGroup.species.inverse() \
                        and utils.getDistance(group,self.target_group) < distance \
                        and group.eff >= self.target_group.eff \
                        and group.eff>groupe_max.eff: #on cherche les groupes ennemis plus proches que nous de la cible, plus nombreux que la cible, et on garde le plus gros d'entre eux
                    groupe_max=group

            enemyWinner = utils.simulateBattle(groupe_max,self.target_group) # on simule une bataille entre ce groupe_max (cad le groupe d'enemis plus proche que nous, ou, à défaut, un groupe fictif vide, qui perdra forcément la bataille)
            winnerFinal = utils.simulateBattle(self.assignedGroup,enemyWinner) # et on simule une bataille entre nous et le gagnant de la première bataille
            #et ensuite on traite les differents cas

            if winnerFinal.species==self.assignedGroup.species: #soit on gagne avec certitude la derniere bataille
                self.possibleEnemyGain = -groupe_max.eff
                self.possibleGain =winnerFinal.eff-self.assignedGroup.eff

            elif winnerFinal.species == Species.human: # soit les humains remportent et nos deux groupes se sont faits bouffer
                self.possibleEnemyGain = -groupe_max.eff
                self.possibleGain = -self.assignedGroup.eff

            else:                                       # soit les enemis gagnent et on perd
                self.possibleEnemyGain = winnerFinal.eff-groupe_max.eff
                self.possibleGain = -self.assignedGroup.eff


        elif self.action_type == ActionType.attackEnemy: #todo ne pas donner une aussi bonne note parce que les ennemis risquent de bouffer des humains plus proches d'eux pour devenir plus gros
            distance = utils.getDistance(self.assignedGroup,self.target_group)
            groupe_max = Group(0,0,0,Species.human) #on initialise un groupe max de base, a 0
            for group in state.groupes:
                if group.species == Species.human \
                        and utils.getDistance(group,self.target_group) < distance \
                        and group.eff < self.target_group.eff \
                        and group.eff>groupe_max.eff: #on cherche les groupes d'humains plus proches que nous de la cible ennemie, moins nombreuse que la cible, et on garde le plus gros d'entre eux
                    groupe_max=group

            enemyWinner = utils.simulateBattle(groupe_max,self.target_group) # on simule une bataille entre ce groupe_max (cad le groupe d'humains plus proche que nous, ou, à défaut, un groupe fictif vide, qui perdra forcément la bataille)
            winnerFinal = utils.simulateBattle(self.assignedGroup,enemyWinner) # et on simule une bataille entre nous et le gagnant de la première bataille

            we_won = (winnerFinal.species==self.assignedGroup.species)
            if we_won:
                self.possibleGain = winnerFinal.eff-self.assignedGroup.eff
                self.possibleEnemyGain = -self.target_group.eff
            else :
                self.possibleGain = -self.assignedGroup.eff
                self.possibleEnemyGain = (winnerFinal.eff-self.target_group.eff)

        elif self.action_type == ActionType.run:  #todo
            self.possibleGain = 0 #todo
        else :
            print("type d'action non reconnu par calc_mark", self.action_type)
        intuitive_mark = (self.possibleGain-self.possibleEnemyGain)
        mark = 0
        if intuitive_mark>=0:
            mark = intuitive_mark/(utils.getDistance(self.assignedGroup,self.target_group))
        else :
            mark = intuitive_mark

        return mark

    def __str__(self):
        return "{} from {} to {}".format(self.action_type, self.assignedGroup, self.target_group)



    def calculateCoup(self, state):
        #dependant on action_type
        #test if below limit lines before sending!!

        if self.action_type ==ActionType.attackHuman:
            #find human group
            grouptoAttack=self.target_group
            vector=utils.getVector(self.assignedGroup,grouptoAttack)
                #here if no split
            return [self.assignedGroup.x, self.assignedGroup.y, self.assignedGroup.eff, self.assignedGroup.x+vector[0], self.assignedGroup.y+vector[1]]
        
        if self.action_type == ActionType.attackEnemy:
            #find  ennemy group
            grouptoAttack=self.target_group
            vector=utils.getVector(self.assignedGroup,grouptoAttack)
                #here if no split
            return [self.assignedGroup.x, self.assignedGroup.y, self.assignedGroup.eff, self.assignedGroup.x+vector[0],self.assignedGroup.y+vector[1]]
 
        if self.action_type == ActionType.run:
            #find closest ennemy group
            grouptoRunfrom=self.target_group
            vector=utils.getVector(self.assignedGroup,grouptoRunfrom)
                #here if no split
            if state.width<(self.assignedGroup.x-vector[0]):
                vector[0]+=1
            elif (self.assignedGroup.x-vector[0]) <0:
                vector[0]-=1 
            if state.height<(self.assignedGroup.y-vector[1]):
                vector[1]-=1 
            elif (self.assignedGroup.y-vector[1]) <0:
                vector[1]+=1

            return [self.assignedGroup.x, self.assignedGroup.y, self.assignedGroup.eff, self.assignedGroup.x-vector[0], self.assignedGroup.y-vector[1]]
