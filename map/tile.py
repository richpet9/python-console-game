import tcod as libtcodpy
import random

class Tile:
    def __init__(self, x, y, building=False):
        self.x = x
        self.y = y
        self.building = building
        self.terrain = "trees" if random.random() < .25 else "grass"

