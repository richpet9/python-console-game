import tcod as libtcodpy
import random

class Tile:
    def __init__(self, x, y, territory=None, building=False):
        self.x = x
        self.y = y
        self.territory = territory
        self.territory_color = libtcodpy.black # Default, error, color
        self.building = building
        self.tree = True if random.random() < .25 else False

    def claimed_by(self, civ_id):
        if(civ_id == 0):
            # Player's civ ID
            # TODO: Extract player color to external file?
            self.territory = "Player"
            self.territory_color = libtcodpy.dark_blue

