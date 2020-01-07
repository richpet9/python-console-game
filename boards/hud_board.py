import tcod as libtcodpy

from boards.board import Board
from workers.construction_worker import read_in_buildings
from util import clamp

class HUDBoard(Board):
    def __init__(self, console, console_width, console_height, player):
        Board.__init__(self, console, console_width, console_height)

        self.entity_count = -1
        self.rendered_objects = -1
        self.buildings = read_in_buildings()
        self.active_building_index = 0
        self.active_building = self.buildings[0] if self.buildings[0] else None
        self.player = player
    
    def render_console(self):
        # Clear the console first
        self.console.clear(ord(' '))

        # Draw the messages
        self.console.print(17, 1, "Entities: " + str(self.entity_count))
        self.console.print(17, 2, "Rendered Objects: " + str(self.rendered_objects))
        
        # Pre-create the cursor string since its a biggin
        cursor = chr(libtcodpy.COLCTRL_2) + 'x' + chr(libtcodpy.COLCTRL_STOP)

        # Print out buildings
        for index, building in enumerate(self.buildings):
            self.console.print(17, index + 3, '[' + (cursor if(index == self.active_building_index) else ' ') + ']' + building["name"])

        # Print out player information
        self.console.print(1, 1, "Funds:%d"%self.player.funds)
        self.console.print(1, 2, "Research:%d"%self.player.research)
        self.console.print(1, 3, "Military:%d"%self.player.military)
        self.console.print(1, 4, "Energy:%d"%self.player.energy)

    def move_active_building(self, amount):
        self.active_building_index = clamp(self.active_building_index + amount, 0, len(self.buildings) - 1)
        self.active_building = self.buildings[self.active_building_index]