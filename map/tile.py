import tcod as libtcodpy
import random

class Tile:
    def __init__(self, x, y, territory_of=None, building=False):
        self.x = x
        self.y = y
        self.territory_of = territory_of
        self.building = building
        self.terrain = "trees" if random.random() < .25 else "grass"

    def claimed_by(self, civ_id):
        # Player's civ ID
        self.territory_of = civ_id

