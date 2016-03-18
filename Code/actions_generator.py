# coding=utf-8                                                                                                                                                                   
from action import Action
from species import Species
from action_type import ActionType
from group import Group
import utils
import math



def enumerate_possible_actions(state, group, specie, number_my_groups, max_split_rate):
    groups_human = state.getMembers(Species.human)
    groups_enemy = state.getMembers(specie.inverse())
    actions_total = []
    len_group_me = group.eff
    actions_simple_per_group = []
    actions_split_per_group = []
    doublets = []
    groups_targets = []

    #on elague les groupes d'humains
    humanDistances = []
    for humangroup in groups_human:
        humanDistances.append(utils.getDistance(group, humangroup))
    groups_human.sort(key=dict(zip(groups_human, humanDistances)).get, reverse=False)
    groups_human=groups_human[:len_group_me+1]

    #de même pour les ennemis
    enemyDistances = []
    for enemy in groups_enemy:
        enemyDistances.append(utils.getDistance(group, enemy))
    groups_enemy.sort(key=dict(zip(groups_enemy, enemyDistances)).get, reverse=False)
    groups_enemy=groups_human[:len_group_me+1]

    # actions sans split
    for group_human in groups_human:
        action = Action(ActionType.attackHuman, group_human, group)
        action.calc_mark(state)
        actions_simple_per_group.append(action)
        groups_targets.append(group_human)

    for group_enemy in groups_enemy:
        action = Action(ActionType.attackEnemy, group_enemy, group)
        action.calc_mark(state)
        actions_simple_per_group.append(action)
        groups_targets.append(group_enemy)

    # actions avec splits
    if number_my_groups <= max_split_rate: #on évite de trop se splitter
        for i in range(1, int(len_group_me/2)+1):
            doublets.append([i, len_group_me-i])

        for doublet in doublets:
            group1 = Group(group.x, group.y, doublet[0], specie)
            group2 = Group(group.x, group.y, doublet[1], specie)
            for target_group_1 in groups_targets:
                action_type_1 = specie.determine_action_type(target_group_1.species)
                for target_group_2 in groups_targets:
                    action_type_2 = specie.determine_action_type(target_group_2.species)
                    # si les deux targets sont différentes :
                    if (target_group_1.x != target_group_2.x) or (target_group_1.y != target_group_2.y):
                        action1 = Action(action_type_1, target_group_1, group1)
                        action2 = Action(action_type_2, target_group_2, group2)
                        action1.calc_mark(state)
                        action2.calc_mark(state)
                        action1.parent_group = group
                        action2.parent_group = group
                        actions_split_per_group.append([action1, action2])
    actions_total.append(actions_simple_per_group)
    actions_total.append(actions_split_per_group)

    return actions_total
