# coding=utf-8                                                                                                                                                                   
from group import Group


def getVector(fromGroup, toGroup):
    distance = [toGroup.x - fromGroup.x, toGroup.y - fromGroup.y]
    norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
    vector= [int(round(distance[0] / norm)),int(round(distance[1] / norm))]
    return vector

