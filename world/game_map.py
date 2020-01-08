import tcod as libtcodpy
import random
import math

from world.tile import Tile
from util import clamp, get_tile_neighbors
from constants import MAP_WIDTH, MAP_HEIGHT



class GameMap:
    '''
    The map is the playable area, displayed in the root console
    '''
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.tiles = [[]]
        self.generate_tiles()

    def generate_tiles(self):
        # Generate all the tiles
        self.tiles = [[Tile(x, y, terrain=("grass" if random.random() < 0.60 else "forest")) for y in range(self.height)] for x in range(self.width)]
        
    def generate_forests(self):
        # Using cellular automata
        # 5 passes are done, B5678/S45678
        for _ in range(0, 5):
            for y in range(MAP_HEIGHT):
                for x in range(MAP_WIDTH):
                    current_tile = self.tiles[x][y]
                    neighbors = get_tile_neighbors(current_tile)
                    total_forest_neighbors = 0

                    for neighbor in neighbors:
                        if(self.tiles[neighbor[0]][neighbor[1]].terrain == "forest"):
                            total_forest_neighbors += 1

                    if(current_tile.terrain != "forest" and total_forest_neighbors > 4):
                        current_tile.terrain = "forest"
                    elif(total_forest_neighbors < 3):
                        current_tile.terrain = "grass"    