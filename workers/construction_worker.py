import tcod as libtcodpy
import json

from entities.building import Building

class ConstructionWorker():
    def __init__(self, tiles, game_entities):
        self.tiles = tiles
        self.game_entities = game_entities
        self.building_list = read_in_buildings()

    def construct_building(self, building, tile):
        # TODO: Make these errors more descript
        if(tile.building): return False
        if(not building): return False

        new_building = Building(tile.x, tile.y, ord(building["char"]), bg=libtcodpy.dark_blue)

        tile.building = building["name"]
        tile.claimed_by(0)
        self.game_entities.append(new_building)

        return True




def read_in_buildings():
    with open("data/buildings.json") as file:
        data = json.load(file)
    
    if(data): return data

    return False


if __name__ == "__main__":
    read_in_buildings()