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
        split1=action_split[0]
        split2=action_split[1]
        merged_actions=action_simple + [1] + [2]
        merged_rates=rate_action_simple + rate_action_split
        merged_actions.sort(key=dict(zip(merged_actions, merged_rates)).get, reverse=True)
        index1=merged_actions.index(1)
        index2=merged_actions.index(2)
        merged_actions[index1]=split1[0]
        merged_actions.insert(index1+1, split1[1])
        merged_actions[index2]=split2[0]
        merged_actions.insert(index2+1, split2[1])
        mission_array.append(merged_actions[-2:])
    newMix=list(itertools.product(*mission_array))
    for mission in newMix:
        newMission = Mission(mission);
        finalArray.append(newMission);

    return finalArray;

    """sortedMissionArray=[]
    for mission in mission_array:
        sortedMissionArray.append([mission,mission.calc_mark(state)])
    sortedMissionArray.sort(key=lambda x: int(x[1]))
    return sortedMissionArray[-5:]"""

def cartesien(list1,list2):
    l3=[[a, b] for a in list1 for b in list2]
    cart2=[]
    for i in l3:
        long = i[0] + [i[1]]
        cart2.append(long)
    return(cart2)

"""    newMix=[[a, b] for a in mission_array[0] for b in mission_array[1]]
    mission_array=mission_array[2:]
    while len(mission_array)>1:
        newMix=cartesien(newMix,mission_array[0])
        mission_array=mission_array[1:]
    newMix=cartesien(newMix,mission_array[0])"""