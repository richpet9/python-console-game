import tcod as libtcodpy
import random

class Tile:
    def __init__(self, x, y, building=False, terrain="grass"):
        self.x = x
        self.y = y
        self.building = building
        self.terrain = terrain
    


