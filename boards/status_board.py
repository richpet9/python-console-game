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
            terrain = self.active_tile.terrain

            self.console.print(1, 1, "[%d, %d]" % (self.active_tile.x, self.active_tile.y))

            if(territory):
                self.console.print(1, 2, territory, fg=self.active_tile.territory_color)
            else:
                self.console.print(1, 2, "unclaimed land", fg=libtcodpy.lighter_gray)

            self.console.print(1, 3, terrain, (libtcodpy.dark_green if terrain == "grass" else libtcodpy.desaturated_green))

            if(building):
                self.console.print(1, 4, building)
                

            

