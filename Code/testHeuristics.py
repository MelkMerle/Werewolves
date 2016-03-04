from IA import Intelligence
from species import Species
from Plateau import PlateauDeJeu

ia = Intelligence()
ia.mySpecie = Species.werewolf

Plateau = PlateauDeJeu(10,10)
Plateau.addGroup(1,1,5,Species.human)
Plateau.addGroup(10,10,5,Species.vampire)
Plateau.addGroup(5,5,10,Species.werewolf)

h = ia.calculateHeuristics(Plateau)
print("L\'heuristique vaut " + str(h))
print(h==5)

