import tcod as libtcodpy

from boards.board import Board
from workers.construction_worker import read_in_buildings
from util import clamp, with_col_code

class HUDBoard(Board):
    def __init__(self, console_width, console_height, player):
        Board.__init__(self, console_width, console_height)

        self.entity_count = -1
        self.rendered_objects = -1
        self.current_turn = -1
        self.buildings = read_in_buildings()
        self.active_building_index = 0
        self.active_building = self.buildings[0] if self.buildings[0] else None
        self.player = player
    
    def render_console(self):
        # Clear the console first
        self.console.clear(ord(' '))

        # Draw the messages
        self.console.print(37, 1, "Entities: " + str(self.entity_count))
        self.console.print(37, 2, "Rendered Objects: " + str(self.rendered_objects))
        self.console.print(37, 3, "Turn: " + str(self.current_turn), fg=libtcodpy.light_amber)
        
        # Pre-create the cursor string since its a biggin
        cursor = with_col_code(2, 'x')

        # Print out buildings
        for index, building in enumerate(self.buildings):
            building_string = building["name"] + ' ' \
                            + with_col_code(3, str(building["cost"])) + ' ' \
                            + with_col_code(5, str(building["energy_requirement"]))
            cursor_string = '[' + (cursor if(index == self.active_building_index) else ' ') + ']'
            self.console.print(10, index + 1, cursor_string + building_string)

        # Print out player information
        self.console.print(1, 1, "F:%d"%self.player.funds, fg=libtcodpy.yellow)
        self.console.print(1, 2, "R:%d"%self.player.research, fg=libtcodpy.cyan)
        self.console.print(1, 3, "M:%d"%self.player.military, fg=libtcodpy.red)
        self.console.print(1, 4, "E:%d"%self.player.energy, fg=libtcodpy.orange)

    def move_active_building(self, amount):
        self.active_building_index = clamp(self.active_building_index + amount, 0, len(self.buildings) - 1)
        self.active_building = self.buildings[self.active_building_index]
    
