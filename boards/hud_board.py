import tcod as libtcodpy

from boards.board import Board
from workers.construction_worker import read_in_buildings
from util import clamp

class HUDBoard(Board):
    def __init__(self, console, console_width, console_height):
        Board.__init__(self, console, console_width, console_height)

        self.entity_count = -1
        self.buildings = read_in_buildings()
        self.active_building_index = 0
        self.active_building = self.buildings[0] if self.buildings[0] else None
    
    def render_console(self):
        # Clear the console first
        self.console.clear(ord(' '))

        # Draw the messages
        self.console.print(1, 1, "Entities: " + str(self.entity_count))
        
        # Pre-create the cursor string since its a biggin
        cursor = chr(libtcodpy.COLCTRL_2) + 'x' + chr(libtcodpy.COLCTRL_STOP)

        for index, building in enumerate(self.buildings):
            self.console.print(1, index + 2, '[' + (cursor if(index == self.active_building_index) else ' ') + ']' + building["name"])

    def move_active_building(self, amount):
        self.active_building_index = clamp(self.active_building_index + amount, 0, len(self.buildings) - 1)
        self.active_building = self.buildings[self.active_building_index]