import tcod as libtcodpy
from map.tile import Tile

class GameMap:
    '''
    The map is the playable area, displayed in the root console
    '''
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.tiles = self.create_tiles()

    def create_tiles(self):
        return [[Tile(x, y) for y in range(self.height)] for x in range(self.width)]
        
