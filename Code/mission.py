# coding=utf-8                                                                                                                                                                   

import utils
import copy
from action_type import ActionType

class Mission:
    def __init__(self, actions):  # Actions is an array of actions
        self.actions=actions

    def calc_mark(self):#calcul de la note ("mark") d'une mission, somme de la note de ses actions (utilisé pour élagage du facteur de branchement
        mark=0
        for action in self.actions:
            mark+=action.mark
        return mark

    def calculateCoup(self, state):
        coupsActions = []
        coupsNombre = 0
        start_positions = []

        for action in self.actions:
            #print(action)
            # ce print peut etre activé pour visualiser les actions qu'on fait a chaque tour
            coup = action.calculateCoup(state)

            #on vérifie qu'on ne "se marche pas dessus", cad une case d'arrivée déjà dans les cases de départ
            start_positions.append([coup[0], coup[1]])
            destination_position = [coup[3], coup[4]]
            if destination_position in start_positions:
                coup = self.evite(coup, action, start_positions, state) #auquel cas, on évite de se chevaucher

            if coup != None:
                coupsActions.append(coup)
                coupsNombre += 1
            else :
                print ("erreur : on essaie de calculer un coup inexistant")

        coups = [coupsNombre, coupsActions]
        return coups

    def evite(self, coup, action, start_positions, state):
        depart = [coup[0], coup[1]]
        cible = [action.target_group.x, action.target_group.y]
        possibles = []

        # On regarde les positions possibles
        for i in range(0, 3):
            for j in range(0, 3):
                position = [depart[0]-1+i, depart[1]-1+j]
                if position not in start_positions:
                    if position[0]<state.width and position[1]<state.height and position[0]>=0 and position[1]>=0:
                        possibles.append(position)

        # Si aucune position possible, le groupe reste sur place
        if len(possibles) == 0:
            return None

        # Sinon on recherche la meilleure position à prendre, en fonction de la cible
        else:
            # On prend la position qui minimise la distance
            # Possiblement améliorable
            pos = None
            distance = 1000
            for position in possibles:
                d = utils.distance(position, cible)
                if d < distance:
                    pos = position
                    distance = d
            coup[3] = pos[0]
            coup[4] = pos[1]
            return coup




    def execute(self,state):

        #il ne faut pas éditer le plateau courant, donc on en fait une copie
        calculatedState = copy.deepcopy(state)

        for action in self.actions: #on parcourt les actions possibles

            # pour les missions de type attackhuman, ou attackenemy on simule l'état du plateau quand on l'aura bouffé
            if action.action_type == ActionType.attackHuman or action.action_type == ActionType.attackEnemy:
                winner = utils.simulateAttackAction(action, state)

                #on vérifie juste si il ya un split, car si il y en a il faut effacer le groupe parent et non le "sous-groupe" qui effectue l'action
                if action.parent_group != None:
                    calculatedState.removeGroup(action.parent_group)
                else :
                    calculatedState.removeGroup(action.assignedGroup)

                calculatedState.removeGroup(action.target_group)
                calculatedState.groupes.append(winner)
            # todo très important, et en retrospect c'est un des points clefs de notre défaite:
            #  améliorer le execute pour une mission attackEnemy, car si l'ennemi est trop loin, on va pas le bouffer car il aura bougé (chose que les humains ne font pas),
            # il ne faut pas simuler une map comme si on l'avait bouffé mais plutot une map ou il est s'est eloigne de nous d'une case et nous nous sommes rapprochés de lui d'une case

            #todo implementer le merge
            if action.action_type == ActionType.merge :
                nouveau_groupe = utils.mergeGroups(action.assignedGroup,action.target_group)
                calculatedState.removeGroup(action.assignedGroup)
                calculatedState.removeGroup(action.target_group)
                calculatedState.groupes.append(nouveau_groupe)

            # todo implementer run
            if action.action_type == ActionType.run :
                groupe_en_action= action.assignedGroup
                groupe_ennemi = action.target_group
                groupe_en_action.x= utils.bordLePlusProche(groupe_en_action,groupe_ennemi)[0] #todo comment simuler le plateau quand on a couru ?
                groupe_en_action.y= utils.bordLePlusProche(groupe_en_action)[1]
                calculatedState.removeGroup(action.assignedGroup)
                calculatedState.removeGroup(action.target_group)
                calculatedState.groupes.append(groupe_en_action)
                calculatedState.groupes.append(groupe_ennemi)

        return calculatedState

    def __str__(self):
        v ="Mission : "
        for action in self.actions:
            v += "\n - " + str(action)
        return v
