from IA import Intelligence
from species import Species
from Plateau import PlateauDeJeu
from group import Group
from actions_generator import enumerate_possible_actions

plateau = PlateauDeJeu(10, 5)

myGroup = Group(4, 1, 4, Species.werewolf)
plateau.addGroup(2,2,4,Species.human)
plateau.addGroup(9,0,2,Species.human)
plateau.addGroup(9,2,1, Species.human)
plateau.addGroup(9,4,2, Species.human)
plateau.addGroup(4,3,4,Species.vampire)
plateau.addThisGroup(myGroup)

print("Enumeration actions ...\n")
actions = enumerate_possible_actions(plateau, myGroup, Species.werewolf)

for actionSimple in actions[0]:
    action_type = actionSimple.action_type
    assigned = actionSimple.assignedGroup
    target = actionSimple.target_group
    print("Action de type " + str(action_type) + " : " + str(assigned) + " vers " + str(target) + ", note : " + str(actionSimple.calc_mark(plateau)))

for twoActions in actions[1]:
    group0 = twoActions[0].assignedGroup
    group1 = twoActions[1].assignedGroup
    print("split " + str(group0.eff) + ", " + str(group1.eff))
    print("   " + str(twoActions[0]) + " : " + str(twoActions[0].calc_mark(plateau)))
    print("   " + str(twoActions[1]) + " : " + str(twoActions[1].calc_mark(plateau)))
