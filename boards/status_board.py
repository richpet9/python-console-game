import tcod as libtcodpy

from boards.board import Board

class StatusBoard(Board):
    def __init__(self, console, console_width, console_height, player):
        Board.__init__(self, console, console_width, console_height)

        # Self.player will eventually be playerS, and we can dictionary search with civ_id
        self.player = player
        self.active_tile = None


    def render_console(self):
        # Clear the board
        self.console.clear(ord(' '))

        # Show active tile info
        if(self.active_tile):
            building = self.active_tile.building
            territory_of = self.active_tile.territory_of
            terrain = self.active_tile.terrain

            self.console.print(1, 1, "[%d, %d]" % (self.active_tile.x, self.active_tile.y))

            if(territory_of is not None):
                self.console.print(1, 2, "Player", fg=self.player.color)
            else:
                self.console.print(1, 2, "unclaimed land", fg=libtcodpy.lighter_gray)

            self.console.print(1, 3, terrain, (libtcodpy.dark_green if terrain == "grass" else libtcodpy.desaturated_green))

            if(building):
                self.console.print(1, 4, building)
                

            

