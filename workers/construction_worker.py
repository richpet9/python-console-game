import tcod as libtcodpy
import json

from entities.building import Building
from util import with_col_code

class ConstructionWorker():
    def __init__(self, tiles, game_entities, player):
        self.tiles = tiles
        self.game_entities = game_entities
        self.player = player
        self.building_list = read_in_buildings()

    def construct_building(self, building, tile):
        if(tile.building): return "Unable to place building, one already exists there."
        if(not building): return "Error: building could not be located in buildings.json"
        if(building["cost"] > self.player.funds): 
            return "This building costs " + \
                    with_col_code(3, str(building["cost"])) + \
                    with_col_code(1, ", you have ") + \
                    with_col_code(3, str(self.player.funds)) + \
                    with_col_code(1, '.')

        # Create the building entitity
        new_building = Building(tile.x, tile.y, ord(building["char"]), bg=libtcodpy.dark_blue)

        # Add turn actions to the building
        if(building["turn_actions"] is not None):
            for action in building["turn_actions"]:
                new_building.add_turn_action(action, building["turn_actions"][action])

        # Tell the tile what it has on it
        tile.building = building["name"]

        # Add the building to game entities
        self.game_entities.append(new_building)

        # Take funds
        self.player.funds += -1 * (building["cost"])

        return True




def read_in_buildings():
    with open("data/buildings.json") as file:
        data = json.load(file)
    
    if(data): return data

    return False


if __name__ == "__main__":
    read_in_buildings()