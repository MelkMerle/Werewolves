from species import Species
from mission_type import MissionType

print(Species.human.inverse() == Species.human)
print(Species.werewolf.inverse() == Species.vampire)
print(Species.vampire.inverse() == Species.werewolf)

print(Species.vampire.determine_mission_type(Species.werewolf) == MissionType.attackEnemy)
print(Species.werewolf.determine_mission_type(Species.vampire) == MissionType.attackEnemy)
print(Species.vampire.determine_mission_type(Species.vampire) == MissionType.merge)
print(Species.werewolf.determine_mission_type(Species.werewolf) == MissionType.merge)
print(Species.werewolf.determine_mission_type(Species.human) == MissionType.attackHuman)
print(Species.vampire.determine_mission_type(Species.human) == MissionType.attackHuman)
print(Species.human.determine_mission_type(Species.human) == MissionType.merge)