from species import Species
from Plateau import PlateauDeJeu
from group import Group
from missions_generator import enumerate_possible_missions

plateau = PlateauDeJeu(5, 5)

plateau.addGroup(4,3,6,Species.vampire)
plateau.addGroup(4,4,4,Species.vampire)
plateau.addGroup(4,0,3,Species.human)
plateau.addGroup(3,0,3,Species.human)
plateau.addGroup(0,4,10,Species.werewolf)

plateau.print_plateau()

missionArray = enumerate_possible_missions(plateau, Species.vampire)

for mission in missionArray:
    print("\n\nNOUVELLE MISSION, note : ", mission.calc_mark(plateau))
    print(mission)
    coup = mission.calculateCoup(plateau)
    print(coup)