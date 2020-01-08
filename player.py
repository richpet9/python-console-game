from tcod import libtcodpy

class Player:
    def __init__(self, name, civ_id, color):
        self.name = name
        self.civ_id = civ_id
        self.color = color

        self.funds = 0
        self.research = 0
        self.military = 0
        self.energy = 0

        self.territory = []

    def claim_tile(self, tile):
        # Check if this tile is already our territory
        if(tile.territory_of is self.civ_id): return

        # Add the tile
        self.territory.append(tile)
        tile.territory_of = self.civ_id
