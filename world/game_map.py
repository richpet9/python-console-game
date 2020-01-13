import tcod as libtcodpy
import random
import math

from world.tile import Tile
from util import clamp, get_tile_neighbors
from constants import MAP_WIDTH, MAP_HEIGHT

NUM_OF_LAKES = 7

class GameMap:
    '''
    The map is the playable area, displayed in the root console
    '''
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.tiles = [[]]
        self.progress = 0

    def generate_tiles(self):
        # Generate all the tiles
        self.tiles = [[Tile(x, y, terrain="grass") for y in range(self.height)] for x in range(self.width)]
        self.generate_lakes()
        self.generate_forests()

    def generate_forests(self):
        # Create random forest tiles
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if(random.random() < 0.40 and self.tiles[x][y].terrain is not "lake"):
                    self.tiles[x][y].terrain = "forest"
        self.progress += 1

        # Using cellular automata
        # 5 passes are done, B5678/S45678
        for _ in range(5):
            for y in range(MAP_HEIGHT):
                for x in range(MAP_WIDTH):
                    current_tile = self.tiles[x][y]
                    neighbors = get_tile_neighbors(current_tile)
                    total_forest_neighbors = 0

                    for neighbor in neighbors:
                        if(self.tiles[neighbor[0]][neighbor[1]].terrain == "forest"):
                            total_forest_neighbors += 1

                    if(current_tile.terrain is not "lake"):
                        if(current_tile.terrain != "forest" and total_forest_neighbors > 4):
                            current_tile.terrain = "forest"
                        elif(total_forest_neighbors < 3):
                            current_tile.terrain = "grass"
        self.progress += 1
    
    def generate_lakes(self):
        # lake_size is a diameter
        lake_size = 2**NUM_OF_LAKES

        # Create random lakes, which are a random gradient of lake tiles from the center to lake_size
        for i in range(NUM_OF_LAKES):
            # Make random point
            random_x = random.randint(0, (MAP_WIDTH - 1) - (lake_size // 2))
            random_y = random.randint(0, (MAP_HEIGHT - 1) - (lake_size // 2))

            for y in range(0, lake_size):
                for x in range(0, lake_size):
                    new_x = clamp((random_x - (lake_size // 2)) + x, 0, MAP_WIDTH - 1)
                    new_y = clamp((random_y - (lake_size // 2)) + y, 0, MAP_HEIGHT - 1)

                    hypoteneuse = math.sqrt((abs(new_x - random_x)**2) + (abs(new_y - random_y)**2))

                    if(random.random() < (((lake_size // 2) - hypoteneuse) / (lake_size // 2)) and hypoteneuse < (lake_size // 2)):
                        self.tiles[new_x][new_y].terrain = "lake"
        
            lake_size -= (2**i)
        self.progress += 1

        # Do cellular automata for the lake tiles (or cells, I guess)
        # B5678 / S45678
        for _ in range(4):
            for y in range(MAP_HEIGHT):
                for x in range(MAP_WIDTH):
                    current_tile = self.tiles[x][y]
                    neighbors = get_tile_neighbors(current_tile)
                    total_lake_neighbors = 0

                    for neighbor in neighbors:
                        if(self.tiles[neighbor[0]][neighbor[1]].terrain == "lake"):
                            total_lake_neighbors += 1

                    if(current_tile.terrain != "lake" and total_lake_neighbors > 4):
                        current_tile.terrain = "lake"
                    elif(total_lake_neighbors < 3):
                        current_tile.terrain = "grass"

            
