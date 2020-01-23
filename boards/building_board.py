import tcod as libtcodpy

from boards.board import Board
from util import clamp, with_col_code

class BuildingBoard(Board):
    def __init__(self, console_width, console_height, player, construction_worker):
        Board.__init__(self, console_width, console_height)
        self.player = player
        self.construction_worker = construction_worker
        self.available_buildings = construction_worker.building_list    # change this to available unlocked ones

        self.active_building = self.available_buildings[0]
        self.active_building_index = 0
    
    def render_console(self):
        # Clear this console
        self.console.clear(ord(' '))

        # Helpful label yes
        self.console.print(1, 1, "BUILDINGS")

        # The offset for building list
        offset = 4

        # Display all the available buildings
        for building in self.available_buildings:
            cursor = ' '
            if(building is self.active_building): 
                cursor = 'X'

            str_building = '[' + with_col_code(3, cursor) + ']' + building["name"]
            self.console.print(1, offset, str_building)
            offset += 1

    def move_active_building(self, amount):
        self.active_building_index = clamp(self.active_building_index + amount, 0, len(self.available_buildings) - 1)
        self.active_building = self.available_buildings[self.active_building_index] 

    def set_active_node(self, index):
        self.active_building_index = index
        self.active_building = self.available_buildings[self.active_building_index]