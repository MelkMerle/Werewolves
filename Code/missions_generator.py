# coding=utf-8


from actions_generator import enumerate_possible_actions
from mission import Mission
import itertools
from species import Species

def enumerate_possible_missions(state, my_species):
    facteur_brch_max = 5
    my_groups = state.getMembers(my_species)

    # on génère la liste de toutes les missions possibles pour chaque groupe de my_groups
    sub_missions_array = generate_group_missions(my_groups, state, my_species)

    #on génère le produit cartésien : i.e. toutes les combinaisons possibles de : une mission assignée par groupe
    possible_strategies=list(itertools.product(*sub_missions_array))
    print "possible missions", possible_strategies

    # on enlève les missions avec redondances, c'est à dire celles où deux groupes alliés prennent pour cible un seul groupe (humain ou enemi)
    final_mission_set = remove_misssions_with_redundancies(possible_strategies)

    # enfin, on trie les stratégies selon leur note, et on fait un dernier élaguage, pour réduire le facteur de branchement
    rate_missions =[]
    for mission in final_mission_set:
        rate_missions.append(mission.calc_mark(state))
    # print final_mission_set,rate_missions
    final_mission_set.sort(key=dict(zip(final_mission_set, rate_missions)).get, reverse=True)
    final_mission_set = final_mission_set[:facteur_brch_max]
    return final_mission_set

def generate_group_missions (groupes, state, species):
    nb_human_groups=len(state.getMembers(Species.human))
    sub_missions_array=[]
    print "nb humans", nb_human_groups
    #on genere une liste de missions possibles par groupe (split et non split)
    for groupMe in groupes:
        possible_actions = enumerate_possible_actions(state, groupMe, species)
        possible_simple_actions = possible_actions[0]
        possible_simple_rates = []
        possible_split_actions = possible_actions[1]
        possible_split_rates = []
        group_missions = []

        for action in possible_simple_actions:
            #on calcule les notes des actions "simples": un groupe attaque un groupe d'humains
            possible_simple_rates.append(action.calc_mark(state))
        for actions in possible_split_actions:
            #on calcule les notes des missions splittées
            possible_split_rates.append(actions[0].calc_mark(state) + actions[1].calc_mark(state))

        #ensuite, on cree notre liste de missions possibles pour ce groupe
        for action in possible_simple_actions:
            group_missions.append(Mission([action]))
        for split_couple in possible_split_actions:
            group_missions.append(Mission([split_couple[0], split_couple[1]]))

        merged_rates = possible_simple_rates + possible_split_rates

        print group_missions, merged_rates

        group_missions.sort(key=dict(zip(group_missions, merged_rates)).get, reverse=True)

        #on rajoute les missions possibles de ce groupe (déjà pré-tronquée) à la liste de sous-missions globales
        sub_missions_array.append(group_missions[:(nb_human_groups*2)]) #todo elaguage pas en fonction du nombre d'humains (genere bugs quand il n'y en a plus), peut etre en fonction de la note ?
    # debug :
    print "submission array", sub_missions_array
    return sub_missions_array

def remove_misssions_with_redundancies(strategies):
    final_possible_strategies=[]
    #chaque stratégie est un tuple de missions, c'est à dire une assignation spécifique d'une mission par groupe
    for mission_tuple in strategies:
        #on reconverti cette assignation de missions sous forme d'une liste d'actions
        missionlist = list(mission_tuple)
        actionList = []
        for mission in missionlist:
            for action in mission.actions:
                actionList.append(action)
        # Et on vérifie qu'il n'y a pas de doublons dans les groupes visés par ces actions
        # auquel cas on fait quoi ??
        target_list=[]
        duplicate_count=0
        for action in actionList:
            if action.target_group not in target_list:
                target_list.append(action.target_group)
            else:
                duplicate_count+=1
        if duplicate_count==0:
            newMission = Mission(actionList)
            final_possible_strategies.append(newMission)
        # else what ? todo implementer merge !
    return final_possible_strategies