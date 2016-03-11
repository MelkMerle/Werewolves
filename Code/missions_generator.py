from actions_generator import enumerate_possible_actions
from mission import Mission


def enumerate_possible_missions(state, my_species):
    mission_array=[]
    my_groups = state.getMembers(my_species)
    for groupMe in my_groups:
        possible_actions = enumerate_possible_actions(state, groupMe, my_species)
        rate_simple = 0
        rate_split = 0
        action_simple = None
        action_split = None

        for action in possible_actions[0]:
            rate = action.calc_mark(state)
            if rate > rate_simple:
                action_simple = action
                rate_simple = rate

        for actions in possible_actions[1]:
            rate = actions[0].calc_mark(state) + actions[1].calc_mark(state)
            if rate > rate_split:
                action_split = actions
                rate_split = rate

        if rate_split > rate_simple:
            mission_array.append(action_split[0])
            mission_array.append(action_split[1])
        else:
            mission_array.append(action_simple)
    newMission = Mission(mission_array);
    return newMission;

    """sortedMissionArray=[]
    for mission in mission_array:
        sortedMissionArray.append([mission,mission.calc_mark(state)])
    sortedMissionArray.sort(key=lambda x: int(x[1]))
    return sortedMissionArray[-5:]"""
