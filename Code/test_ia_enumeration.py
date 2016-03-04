from IA import Intelligence
from species import Species
from Plateau import PlateauDeJeu
from group import Group


ia = Intelligence()
ia.mySpecie = Species.werewolf

plateau = PlateauDeJeu(10,10)

myGroup = Group(9,9,10,Species.werewolf)
plateau.addGroup(1,1,5,Species.human)
plateau.addGroup(2,2,5,Species.human)
plateau.addGroup(3,4,12, Species.human)
plateau.addGroup(9,9,5,Species.vampire)
plateau.addThisGroup(myGroup)

print("Enumeration actions ...\n")
actions = ia.enumeratePossibleActions(plateau, myGroup)

for actionSimple in actions[0]:
    mission_type = actionSimple.mission_type
    assigned = actionSimple.assignedGroup
    target = actionSimple.target_group
    print("Action de type " + str(mission_type) + " : " + str(assigned) + " vers " + str(target) + ", note : " + str(actionSimple.calc_mark()))

for twoActions in actions[1]:
    group0 = twoActions[0].assignedGroup
    group1 = twoActions[1].assignedGroup
    print("split " + str(group0.eff) + ", " + str(group1.eff))
    print("     Action de type " + str(twoActions[0].mission_type) + " : " + str(group0) + " vers " + str(twoActions[0].target_group) + "note : " + str(twoActions[0].calc_mark()))
    print("     Action de type " + str(twoActions[1].mission_type) + " : " + str(group1) + " vers " + str(twoActions[1].target_group) + "note : " + str(twoActions[1].calc_mark()))