from IA import Intelligence
from species import Species
from Plateau import PlateauDeJeu
from group import Group
from actions_generator import enumerate_possible_actions

plateau = PlateauDeJeu(10,10)

myGroup = Group(9,9,10,Species.werewolf)
plateau.addGroup(1,1,5,Species.human)
plateau.addGroup(2,2,5,Species.human)
plateau.addGroup(3,4,12, Species.human)
plateau.addGroup(9,9,5,Species.vampire)
plateau.addThisGroup(myGroup)

print("Enumeration actions ...\n")
actions = enumerate_possible_actions(plateau, myGroup, Species.werewolf)

for actionSimple in actions[0]:
    mission_type = actionSimple.mission_type
    assigned = actionSimple.assignedGroup
    target = actionSimple.target_group
    print("Action de type " + str(mission_type) + " : " + str(assigned) + " vers " + str(target) + ", note : " + str(actionSimple.calc_mark(plateau)))

for twoActions in actions[1]:
    group0 = twoActions[0].assignedGroup
    group1 = twoActions[1].assignedGroup
    print("split " + str(group0.eff) + ", " + str(group1.eff))
    print("     Action de type " + str(twoActions[0].mission_type) + " : " + str(group0) + " vers " + str(twoActions[0].target_group) + "note : " + str(twoActions[0].calc_mark(plateau)))
    print("     Action de type " + str(twoActions[1].mission_type) + " : " + str(group1) + " vers " + str(twoActions[1].target_group) + "note : " + str(twoActions[1].calc_mark(plateau)))
