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
        self.player = player
    
    def render_console(self):
        # Clear the console first
        self.console.clear(ord(' '))

        # Draw the messages
        self.console.print(37, 1, "Entities: " + str(self.entity_count))
        self.console.print(37, 2, "Rendered Objects: " + str(self.rendered_objects))
        self.console.print(37, 3, "Turn: " + str(self.current_turn), fg=libtcodpy.light_amber)
        

        # Print out player information
        self.console.print(1, 1, "F:%d"%self.player.funds, fg=libtcodpy.yellow)
        self.console.print(1, 2, "R:%d"%self.player.research, fg=libtcodpy.cyan)
        self.console.print(1, 3, "M:%d"%self.player.military, fg=libtcodpy.red)
        self.console.print(1, 4, "E:%d"%self.player.energy, fg=libtcodpy.orange)
    
