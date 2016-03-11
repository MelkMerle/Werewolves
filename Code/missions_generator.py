from actions_generator import enumerate_possible_actions
from mission import Mission


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
            rate = action.calc_mark(state)
            if (rate > rate_action_simple[0]):
                action_simple [0]= action
                rate_action_simple[0] = rate
            elif (rate > rate_action_simple[1]):
                action_simple [1]= action
                rate_action_simple[1] = rate

        for actions in possible_actions[1]:
            rate = actions[0].calc_mark(state) + actions[1].calc_mark(state)
            if rate > rate_action_split[0]:
                action_split[0] = actions
                rate_action_split[0] = rate
            elif rate > rate_action_split[1]:
                action_split[1] = actions
                rate_action_split[1] = rate

        merged_actions=action_simple + action_split
        merged_rates=rate_action_simple + rate_action_split
        merged_actions.sort(key=dict(zip(merged_actions, merged_rates)).get)
        mission_array.append(merged_actions[-2:])

    newMission = Mission(mission_array);
    finalArray.append(newMission);
    return finalArray;

    """sortedMissionArray=[]
    for mission in mission_array:
        sortedMissionArray.append([mission,mission.calc_mark(state)])
    sortedMissionArray.sort(key=lambda x: int(x[1]))
    return sortedMissionArray[-5:]"""

def product(*args, **kwds):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = map(tuple, args) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)
