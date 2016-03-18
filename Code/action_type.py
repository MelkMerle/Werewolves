# coding=utf-8

from enum import Enum

class ActionType(Enum):
    attackEnemy = 'attackEnemy'
    attackHuman = 'attackHuman'
    merge = 'merge'
    run = 'run'
