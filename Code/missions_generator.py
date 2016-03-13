from actions_generator import enumerate_possible_actions
from mission import Mission
import itertools

def enumerate_possible_missions(state, my_species):
    mission_array=[]
    finalArray=[]
    my_groups = state.getMembers(my_species)
    for groupMe in my_groups:
        possible_actions = enumerate_possible_actions(state, groupMe, my_species)
        action_simple = [None, None]
        action_split = [None, None]
        rate_action_simple = [-1000, -1000]
        rate_action_split = [-1000, -1000]

        for action in possible_actions[0]:
            #on gère les actions "simples": un groupe attaque un groupe d'humains
            rate = action.calc_mark(state)
            if (rate > rate_action_simple[0]):
                action_simple [0]= action
                rate_action_simple[0] = rate
            elif (rate > rate_action_simple[1]):
                action_simple [1]= action
                rate_action_simple[1] = rate

        for actions in possible_actions[1]:
            #on gère les missions splittés
            rate = actions[0].calc_mark(state) + actions[1].calc_mark(state)
            if rate > rate_action_split[0]:
                action_split[0] = actions
                rate_action_split[0] = rate
            elif rate > rate_action_split[1]:
                action_split[1] = actions
                rate_action_split[1] = rate
        #contournement de l'impossibilité de trier une liste de liste. estion de l'exception des actions splittées
        split1=action_split[0]
        split2=action_split[1]
        merged_actions=action_simple + [1] + [2]
        merged_rates=rate_action_simple + rate_action_split
        #classement des actions pour un groupe
        merged_actions.sort(key=dict(zip(merged_actions, merged_rates)).get, reverse=True)
        index1=merged_actions.index(1)
        merged_actions[index1]=split1[0]
        merged_actions.insert(index1+1, split1[1])
        index2=merged_actions.index(2)
        merged_actions[index2]=split2[0]
        merged_actions.insert(index2+1, split2[1])
        if merged_actions[0]==None:
            break
        elif merged_actions[1]==None:
            mission_array.append((merged_actions[-1:]))
        else:
            mission_array.append(merged_actions[-2:])
            #on renvoie le top 2 des meilleures actions de chaque groupe

    #on sort toutes le combinaisons possibles
    newMix=list(itertools.product(*mission_array))
    for mission in newMix:
        newMission = Mission(mission);
        finalArray.append(newMission);
    return finalArray;
