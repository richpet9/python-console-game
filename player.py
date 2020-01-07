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