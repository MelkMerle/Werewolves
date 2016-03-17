from species import Species
from Plateau import PlateauDeJeu
from group import Group
from missions_generator import enumerate_possible_missions

plateau = PlateauDeJeu(13, 5)

myGroup = Group(4, 1, 4, Species.werewolf)
plateau.addGroup(2,2,4,Species.human)
plateau.addGroup(9,0,2,Species.human)
plateau.addGroup(9,2,2, Species.human)
plateau.addGroup(9,1,2,Species.human)
plateau.addGroup(9,3,2,Species.human)
plateau.addGroup(9,4,2,Species.human)

plateau.addGroup(12,1,3, Species.vampire)
plateau.addGroup(12,3,3, Species.werewolf)

plateau.addGroup(4,3,4,Species.vampire)
plateau.addThisGroup(myGroup)

# plateau = PlateauDeJeu(5, 6)
# myGroup = Group(5, 4, 2, Species.werewolf)
# plateau.addGroup(4,4,2,Species.werewolf)
# plateau.addGroup(3,4,1,Species.human)
# plateau.addGroup(2,4,1,Species.human)
# plateau.addGroup(2,2,1,Species.human)
# #plateau.addGroup(9,2,1, Species.human)
# #plateau.addGroup(9,4,2, Species.human)
# plateau.addGroup(1,1,3,Species.vampire)
# plateau.addThisGroup(myGroup)

# plateau = PlateauDeJeu(10, 5)
#
# myGroup = Group(4, 1, 4, Species.werewolf)
# plateau.addGroup(2,2,4,Species.human)
# plateau.addGroup(9,0,2,Species.human)
# plateau.addGroup(9,2,1, Species.human)
# plateau.addGroup(9,4,2, Species.human)
# plateau.addGroup(4,3,4,Species.vampire)
# plateau.addThisGroup(myGroup)

plateau.print_plateau()
missionArray = enumerate_possible_missions(plateau, Species.werewolf, 4)

for mission in missionArray:
    print("\nthis is a mission de note : " + str(mission.calc_mark()))
    # coup = mission.calculateCoup(plateau)
    for action in mission.actions:
        action_type = action.action_type
        assigned = action.assignedGroup
        target = action.target_group
        print("Action de type " + str(action_type) + " : " + str(assigned) + " vers " + str(target)+" note : " + str(action.mark))

    newstate= mission.execute(plateau)

    newstate.print_plateau()