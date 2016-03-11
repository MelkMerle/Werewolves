"""from species import Species
from Plateau import PlateauDeJeu
from group import Group
from missions_generator import enumerate_possible_missions

plateau = PlateauDeJeu(10,10)

myGroup = Group(9, 9, 10, Species.werewolf)
plateau.addGroup(1, 1, 8, Species.human)
plateau.addGroup(2, 2, 2, Species.human)
plateau.addGroup(3, 4, 12, Species.human)
plateau.addGroup(9, 9, 5, Species.vampire)
plateau.addThisGroup(myGroup)

missionArray = enumerate_possible_missions(plateau, Species.werewolf)

print(missionArray)

for action in missionArray:
    mission_type = action.mission_type
    assigned = action.assignedGroup
    target = action.target_group
    print("Action de type " + str(mission_type) + " : " + str(assigned) + " vers " + str(target))

"""
l1=[1,3,5]
l2=[2,4,7]
l3=sorted(l1 + l2)

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

print([[a, b, c] for a in [1,2,3] for b in ['a','b'] for c in [4,5]])

