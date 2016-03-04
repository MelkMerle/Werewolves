from species import Species
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