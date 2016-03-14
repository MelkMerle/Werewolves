from species import Species
from Plateau import PlateauDeJeu
from group import Group
from missions_generator import enumerate_possible_missions

plateau = PlateauDeJeu(10, 5)

myGroup = Group(4, 1, 4, Species.werewolf)
plateau.addGroup(2,2,4,Species.human)
plateau.addGroup(9,0,2,Species.human)
plateau.addGroup(9,2,1, Species.human)
plateau.addGroup(12,2,2, Species.werewolf)
plateau.addGroup(12,2,3, Species.werewolf)

plateau.addGroup(4,3,4,Species.vampire)
plateau.addGroup(2,1,5,Species.vampire)
plateau.addThisGroup(myGroup)

missionArray = enumerate_possible_missions(plateau, Species.werewolf)

print(missionArray)
print(len(missionArray))

for mission in missionArray:
    print("this is a mission")
    for action in mission.actions:
        action_type = action.action_type
        assigned = action.assignedGroup
        target = action.target_group
        print("Action de type " + str(action_type) + " : " + str(assigned) + " vers " + str(target))