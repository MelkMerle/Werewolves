# coding=utf-8


from actions_generator import enumerate_possible_actions
from mission import Mission
import itertools
from species import Species

def enumerate_possible_missions(state, my_species, branchement, split_rate):
    facteur_brch_max = branchement
    my_groups = state.getMembers(my_species)

    # on génère la liste de toutes les missions possibles pour chaque groupe de my_groups
    sub_missions_array = generate_group_missions(my_groups, state, my_species,split_rate)

    #on génère le produit cartésien : i.e. toutes les combinaisons possibles de : une mission assignée par groupe
    possible_strategies=list(itertools.product(*sub_missions_array))

    # on enlève les missions avec redondances, c'est à dire celles où deux groupes alliés prennent pour cible un seul groupe (humain ou enemi)
    final_mission_set = remove_missions_with_redundancies(possible_strategies)

    # enfin, on trie les stratégies selon leur note, et on fait un dernier élaguage, pour réduire le facteur de branchement
    rate_missions =[]
    for mission in final_mission_set:
        rate_missions.append(mission.calc_mark())
    final_mission_set.sort(key=dict(zip(final_mission_set, rate_missions)).get, reverse=True)
    final_mission_set = final_mission_set[:facteur_brch_max]

    return final_mission_set

def generate_group_missions (groupes, state, species, max_split_rate):
    nb_human_groups=len(state.getMembers(Species.human))
    nb_enemy_groups=len(state.getMembers(species.inverse()))
    nb_my_groups = len(groupes)
    sub_missions_array=[]
    #on genere une liste de missions possibles par groupe (split et non split)
    for groupMe in groupes:
        possible_actions = enumerate_possible_actions(state, groupMe, species,nb_my_groups, max_split_rate)


        possible_simple_actions = possible_actions[0]
        possible_simple_rates = []
        possible_split_actions = possible_actions[1]
        possible_split_rates = []
        group_missions = []

        for action in possible_simple_actions:
             #on calcule les notes des actions "simples": un groupe attaque un groupe d'humains
             action.calc_mark(state)
             possible_simple_rates.append(action.mark)
        for actions in possible_split_actions:
             #on calcule les notes des missions splittées
             actions[0].calc_mark(state)
             actions[1].calc_mark(state)
             possible_split_rates.append(actions[0].mark + actions[1].mark)

        #ensuite, on cree notre liste de missions possibles pour ce groupe
        for action in possible_simple_actions:
            group_missions.append(Mission([action]))
        for split_couple in possible_split_actions:
            group_missions.append(Mission([split_couple[0], split_couple[1]]))

        merged_rates = possible_simple_rates + possible_split_rates


        group_missions.sort(key=dict(zip(group_missions, merged_rates)).get, reverse=True)

        #on rajoute les missions possibles de ce groupe (déjà pré-tronquée) à la liste de sous-missions globales
        sub_missions_array.append(group_missions[:(nb_human_groups+nb_enemy_groups)])

    return sub_missions_array

def remove_missions_with_redundancies(strategies):
    final_possible_strategies=[]

    #chaque stratégie est un tuple de missions, c'est à dire une assignation spécifique d'une mission par groupe
    while len(strategies)>1: #on parcourt la liste des stratégies, et on elève celles qui ont des doublons
        mission_tuple = strategies[-1]
        strategies.pop()
        #on reconverti cette assignation de missions sous forme d'une liste d'actions
        actionList= convertStratToActions(mission_tuple)
        # Et on vérifie qu'il n'y a pas de doublons dans les groupes visés par ces actions
        target_list=[]
        duplicate_count=0
        for action in actionList:
            if action.target_group not in target_list:
                target_list.append(action.target_group)
            else: #todo plutot que de l'effacer brutalement, implementer merge
                duplicate_count+=1
        if duplicate_count==0:
            newMission = Mission(actionList)
            final_possible_strategies.append(newMission)
    final_possible_strategies.append(Mission(convertStratToActions(strategies[0]))) #mais, quoi qu'il arrive, on rajoute toujours au moins une stratégie

    return final_possible_strategies

def convertStratToActions(strategy):
    missionlist = list(strategy)
    actionList = []
    for mission in missionlist:
        for action in mission.actions:
            actionList.append(action)
    return actionList
