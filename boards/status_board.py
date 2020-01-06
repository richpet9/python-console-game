import tcod as libtcodpy

from boards.board import Board

class StatusBoard(Board):
    def __init__(self, console, console_width, console_height):
        Board.__init__(self, console, console_width, console_height)

        self.active_tile = None

    def render_console(self):
        # Clear the board
        self.console.clear(ord(' '))

        # Show active tile info
        if(self.active_tile):
            building = self.active_tile.building
            territory = self.active_tile.territory
            # terrain = self.active_tile.terrain

            self.console.print(1, 1, "[%d, %d]" % (self.active_tile.x, self.active_tile.y))
            self.console.print(1, 2, (building if building else "no building"))
            self.console.print(1, 3, (territory if territory else "unclaimed land"))

