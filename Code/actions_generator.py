# coding=utf-8                                                                                                                                                                   
from action import Action
from species import Species
from mission_type import MissionType
from group import Group


def enumerate_possible_actions(state, group, specie):
    groups_human = state.getMembers(Species.human)
    groups_enemy = state.getMembers(specie.inverse())
    actions_total = []
    len_group_me = group.eff
    actions_simple_per_group = []
    actions_split_per_group = []
    doublets = []
    # actions sans split
    for group_human in groups_human:
        action = Action(MissionType.attackHuman, group_human, group)
        actions_simple_per_group.append(action)
    for group_enemy in groups_enemy:
        action = Action(MissionType.attackEnemy, group_enemy, group)
        actions_simple_per_group.append(action)

    # actions avec splits
    for i in range(1, int(len_group_me/2)+1):
        doublets.append([i, len_group_me-i])
    groups_targets = groups_human + groups_enemy
    for doublet in doublets:
        group1 = Group(group.x, group.y, doublet[0], specie)
        group2 = Group(group.x, group.y, doublet[1], specie)
        for target_group_1 in groups_targets:
            mission_type_1 = specie.determine_mission_type(target_group_1.species)
            for target_group_2 in groups_targets:
                mission_type_2 = specie.determine_mission_type(target_group_2.species)
                if target_group_1 != target_group_2:
                    action1 = Action(mission_type_1, target_group_1, group1)
                    action2 = Action(mission_type_2, target_group_2, group2)
                    actions_split_per_group.append([action1, action2])
    actions_total.append(actions_simple_per_group)
    actions_total.append(actions_split_per_group)
    return actions_total
