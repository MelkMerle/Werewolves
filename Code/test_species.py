from species import Species

print(Species.human.inverse()==Species.human)
print(Species.werewolf.inverse()==Species.vampire)
print(Species.vampire.inverse()==Species.werewolf)

