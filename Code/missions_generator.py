# coding=utf-8

from actions_generator import enumerate_possible_actions
from mission import Mission
import itertools
from species import Species

def enumerate_possible_missions(state, my_species):
    actions_array=[]
    finalArray=[]
    my_groups = state.getMembers(my_species)
    nb_human_groups=len(state.getMembers(Species.human))
    nb_groups=len(my_groups)
    facteur_brch_max=4
    for groupMe in my_groups:
        possible_actions = enumerate_possible_actions(state, groupMe, my_species)
        possible_simple_actions = possible_actions[0]
        possible_simple_rates = []
        possible_split_actions = possible_actions[1]
        possible_split_rates = []
        split_list_index = []

        for action in possible_simple_actions:
            #on gère les actions "simples": un groupe attaque un groupe d'humains
            possible_simple_rates.append(action.calc_mark(state))

        for actions in possible_split_actions:
            #on gère les missions splittés
            possible_split_rates.append(actions[0].calc_mark(state) + actions[1].calc_mark(state))
        for i in range(len(possible_split_actions)):
            split_list_index.append(i)
        merged_actions = possible_simple_actions + split_list_index
        merged_rates = possible_simple_rates + possible_split_rates
        merged_actions.sort(key=dict(zip(merged_actions, merged_rates)).get, reverse=True)
        if len(merged_actions)>(nb_human_groups*2):
            merged_actions=merged_actions[-(nb_human_groups*2):]
        for element in merged_actions:
            if element in split_list_index:
                newIndex=merged_actions.index(element)
                merged_actions[newIndex] = possible_split_actions[element][0]
                merged_actions.insert(newIndex, possible_split_actions[element][1])
        if len(merged_actions)>(nb_human_groups*2):
            actions_array.append(merged_actions[-(nb_human_groups*2):])
        else:
            actions_array.append(merged_actions)


    #on sort toutes le combinaisons possibles
    newMix=list(itertools.product(*actions_array))
    rate_missions=[]
    saved_missions=[]
    for mission in newMix:
        for element in mission:
            if type(element) is list:
                index = mission.index(element)
                element = element[0]
                mission.insert(index,element[1])
        #On vérifie qu'il n'y a pas de doublons dans les action.targetgroup

        target_list=[]
        duplicate_count=0
        for action in mission:
            if action.target_group not in target_list:
                target_list.append(action.target_group)
            else:
                duplicate_count+=1
        if duplicate_count==0:
            newMission = Mission(mission)
            saved_missions.append(newMission)
            rate_missions.append(newMission.calc_mark(state))
            print(newMission.calc_mark(state))
    saved_missions.sort(key=dict(zip(saved_missions, rate_missions)).get, reverse=True)
    saved_missions=saved_missions[-facteur_brch_max:]
    return saved_missions

