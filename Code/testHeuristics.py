
from species import Species
from group import Group

class PlateauDeJeu:

    def __init__(self,width,height):
        self.groupes = []
        self.width=width
        self.height=height

    def getGroup(self, x, y):
        for groupe in self.groupes:
            if (groupe.x==x & groupe.y==y):
                return groupe
        print("Aucun groupe n'a été trouvé par la méthode getGroup")
        return None

    def addGroup(self,x, y, effectif, espece):
        nouveau = Group(x, y, effectif, espece)
        self.groupes.append(nouveau)
        return nouveau

    def getMembers(self, espece):
        members = []
        for group in self.groupes:
            if group.species == espece:
                members.append(group)
        return members

def calculateHeuristics(state, myspecie):
    # here we do so mathematics voodoo
    heuristics=0
    wwGroups=state.getMembers(Species.werewolf)
    vpGroups=state.getMembers(Species.vampire)
    wwNumber=0
    vpNumber=0
    for g in wwGroups:
        wwNumber=wwNumber + g.eff
    for g in vpGroups:
        vpNumber=vpNumber + g.eff

    if (myspecie==Species.werewolf):
        heuristics=wwNumber-vpNumber
    else:
        heuristics=vpNumber-wwNumber
    return heuristics

Plateau = PlateauDeJeu(10,10)
Plateau.addGroup(1,1,5,Species.human)
Plateau.addGroup(10,10,5,Species.vampire)
Plateau.addGroup(5,5,10testHeuristics.py,Species.werewolf)

h = calculateHeuristics(Plateau, 'vampire')
print('coucou')
print(h)
