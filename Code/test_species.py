from species import Species
from action_type import ActionType

print(Species.human.inverse() == Species.human)
print(Species.werewolf.inverse() == Species.vampire)
print(Species.vampire.inverse() == Species.werewolf)

print(Species.vampire.determine_action_type(Species.werewolf) == ActionType.attackEnemy)
print(Species.werewolf.determine_action_type(Species.vampire) == ActionType.attackEnemy)
print(Species.vampire.determine_action_type(Species.vampire) == ActionType.merge)
print(Species.werewolf.determine_action_type(Species.werewolf) == ActionType.merge)
print(Species.werewolf.determine_action_type(Species.human) == ActionType.attackHuman)
print(Species.vampire.determine_action_type(Species.human) == ActionType.attackHuman)
print(Species.human.determine_action_type(Species.human) == ActionType.merge)