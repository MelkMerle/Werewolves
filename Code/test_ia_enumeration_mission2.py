from species import Species
from Plateau import PlateauDeJeu
from group import Group
from missions_generator import enumerate_possible_missions
import itertools




plateau = PlateauDeJeu()
plateau.width=10
plateau.height=10

myGroup = Group(9, 9, 10, Species.werewolf)
plateau.addGroup(1, 1, 8, Species.human)
plateau.addGroup(2, 2, 2, Species.human)
plateau.addGroup(3, 4, 12, Species.human)
plateau.addGroup(9, 9, 5, Species.vampire)
plateau.addGroup(8, 9, 5, Species.werewolf)
plateau.addGroup(7, 9, 5, Species.werewolf)
plateau.addGroup(6, 9, 5, Species.werewolf)
plateau.addGroup(5, 9, 5, Species.werewolf)
plateau.addThisGroup(myGroup)

missionArray = enumerate_possible_missions(plateau, Species.werewolf)

print(missionArray)

for mission in missionArray:
    for action in mission.actions:
        print(action)
        mission_type = action.mission_type
        assigned = action.assignedGroup
        target = action.target_group
        print("Action de type " + str(mission_type) + " : " + str(assigned) + " vers " + str(target))





"""def product(*args, **kwds):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = map(tuple, args) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)
"""

"""def product(*args, **kwds):
    "Alternative fast implementation of product for python < 2.6"
    def cycle(sequence, uplevel):
        while True:
            vals = next(uplevel)   # advance upper level, raises if done
            it = iter(sequence)    # (re-)start iteration of current level
            try:
                while True: yield vals + (next(it),)
            except StopIteration:
                pass

    step = iter(((),))
    for pool in map(tuple, args)*kwds.get('repeat', 1):
        step = cycle(pool, step)   # build stack of iterators
    return step

L=product('ABCD','123')"""



"""def cartesien(list1,list2):
    l3=[[a, b] for a in list1 for b in list2]
    cart2=[]
    for i in l3:
        long = i[0] + [i[1]]
        cart2.append(long)
    return(cart2)

newMix=[[a, b] for a in missionArray[0] for b in missionArray[1]]
missionArray=missionArray[2:]


while len(missionArray)>1:
    newMix=cartesien(newMix,missionArray[0])
    missionArray=missionArray[1:]
newMix=cartesien(newMix,missionArray[0])
print(newMix)
"""


