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


        # First we select some random tiles, based off diagonal size of the map
        # number_of_seeds = int(math.sqrt((MAP_WIDTH**2) + (MAP_HEIGHT**2)))
        # number_of_seeds = 2

        # for _ in range(number_of_seeds):
        #     # Get a random tile on the map
        #     random_tile_x = random.randint(0, MAP_WIDTH - 1)
        #     random_tile_y = random.randint(0, MAP_HEIGHT - 1)

        #     # Randomlly decide the size of the forest
        #     size = -1
        #     size_controller = random.random()

        #     if(size_controller < 0.20):
        #         # 20% chance of being a small forest
        #         size = random.randint(FOREST_SMALL - (FOREST_SMALL // 2), FOREST_SMALL + (FOREST_SMALL // 2))
        #     elif(size_controller > 0.20 and size_controller <= 0.25):
        #         # 5% chance of being a huge forest
        #         size = random.randint(FOREST_HUGE - (FOREST_HUGE // 2), FOREST_HUGE + (FOREST_HUGE // 2))
        #     else:
        #         # 75% chance of being an average forest
        #         size = random.randint(FOREST_AVG - (FOREST_AVG // 2), FOREST_AVG + (FOREST_AVG // 2))

        #     far_left_x = clamp((random_tile_x - (size // 2)), 0, MAP_WIDTH - 1)
        #     far_left_y = clamp((random_tile_y + random.randint(-5, 5)), 0, MAP_HEIGHT - 1)

        #     far_right_x = clamp((random_tile_x + (size // 2)), 0, MAP_WIDTH - 1)
        #     far_right_y = clamp((random_tile_y + random.randint(-5, 5)), 0, MAP_HEIGHT - 1)

        #     far_top_x = clamp((random_tile_x + random.randint(-5, 5)), 0, MAP_WIDTH - 1)
        #     far_top_y = clamp((random_tile_y - (size // 2)), 0, MAP_HEIGHT - 1)

        #     far_bottom_x = clamp((random_tile_x + random.randint(-5, 5)), 0, MAP_WIDTH - 1)
        #     far_bottom_y = clamp((random_tile_y + (size // 2)), 0, MAP_HEIGHT - 1)

        #     for y in range(far_top_y, far_bottom_y):
        #         for x in range(0, y):
        #             self.tiles[(random_tile_x - y) + x][y].terrain = "forest"




