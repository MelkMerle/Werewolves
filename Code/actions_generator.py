# coding=utf-8                                                                                                                                                                   
from action import Action
from species import Species
from mission_type import MissionType
from group import Group


def enumerate_possible_actions(state, group, my_species):
    groups_human = state.getMembers(Species.human)
    groups_enemy = state.getMembers(my_species.inverse())
    actions_total = []
    len_group_me = group.eff
    actions_simple_per_group = []
    actions_split_per_group = []
    doublets = []
    groups_targets = []
    # actions sans split
    for group_human in groups_human:
        action = Action(MissionType.attackHuman, group_human, group)
        actions_simple_per_group.append(action)
        groups_targets.append(group_human)
    for group_enemy in groups_enemy:
        action = Action(MissionType.attackEnemy, group_enemy, group)
        actions_simple_per_group.append(action)
        groups_targets.append(group_enemy)

    # actions avec splits
    for i in range(1, int(len_group_me/2)+1):
        doublets.append([i, len_group_me-i])

    for doublet in doublets:
        group1 = Group(group.x, group.y, doublet[0], my_species)
        group2 = Group(group.x, group.y, doublet[1], my_species)
        for target_group_1 in groups_targets:
            mission_type_1 = my_species.determine_mission_type(target_group_1.species)
            for target_group_2 in groups_targets:
                mission_type_2 = my_species.determine_mission_type(target_group_2.species)
                # si les deux targets sont différentes :
                if target_group_1.x != target_group_2.x and target_group_1.y != target_group_2.y:
                    action1 = Action(mission_type_1, target_group_1, group1)
                    action2 = Action(mission_type_2, target_group_2, group2)
                    actions_split_per_group.append([action1, action2])
    actions_total.append(actions_simple_per_group)
    actions_total.append(actions_split_per_group)

    return actions_total