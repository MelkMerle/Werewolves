from species import Species
from Plateau import PlateauDeJeu
from group import Group
from missions_generator import enumerate_possible_missions

plateau = PlateauDeJeu(5, 5)


plateau.addGroup(2,2,4,Species.vampire)
plateau.addGroup(1,2,4,Species.vampire)
plateau.addGroup(4,2,3,Species.human)
plateau.addGroup(3,2,3,Species.human)
plateau.addGroup(1,4,10,Species.werewolf)


missionArray = enumerate_possible_missions(plateau, Species.vampire)

for mission in missionArray:
    print("\n\nNOUVELLE MISSION, note : ", mission.calc_mark(plateau))
    coup = mission.calculateCoup(plateau)
