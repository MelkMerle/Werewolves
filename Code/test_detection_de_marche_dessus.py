from species import Species
from Plateau import PlateauDeJeu
from group import Group
from missions_generator import enumerate_possible_missions

plateau = PlateauDeJeu(5, 5)


<<<<<<< bade148ff60aaae0f17190fc4a43b14730cd2a38
plateau.addGroup(0,2,4,Species.vampire)
=======
plateau.addGroup(2,2,4,Species.vampire)
>>>>>>> detection de chevauchement
plateau.addGroup(1,2,4,Species.vampire)
plateau.addGroup(4,2,3,Species.human)
plateau.addGroup(3,2,3,Species.human)
plateau.addGroup(1,4,10,Species.werewolf)

<<<<<<< bade148ff60aaae0f17190fc4a43b14730cd2a38
plateau.print()
=======
>>>>>>> detection de chevauchement

missionArray = enumerate_possible_missions(plateau, Species.vampire)

for mission in missionArray:
    print("\n\nNOUVELLE MISSION, note : ", mission.calc_mark(plateau))
<<<<<<< bade148ff60aaae0f17190fc4a43b14730cd2a38
    print(mission)
    coup = mission.calculateCoup(plateau)

=======
    coup = mission.calculateCoup(plateau)
>>>>>>> detection de chevauchement
