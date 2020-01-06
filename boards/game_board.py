import tcod as libtcodpy

from boards.board import Board

class GameBoard(Board):
    def __init__(self, console, console_width, console_height, game_map):
        Board.__init__(self, console, console_width, console_height)

        self.game_map = game_map

    def render_console(self):
        # Clear the board
        self.console.clear(ord(' '))
        
        # Render the tiles in the map
        for y in range(0, self.game_map.height):
            for x in range(0, self.game_map.width):
                self.render_tile(x, y)

    def render_tile(self, x, y):
        # Get the tile we want to render from the map
        tile = self.game_map.tiles[x][y]

        if(not tile.territory):
            # If the tile is not a building, or territory, render is as a green block (grass)
            self.console.print(x, y, 'G', [125, 160, 120], [25, 60, 20])
        else:
            # Tile is territory, so show the background of the owner
            self.console.print(x, y, ' ', bg=tile.territory_color)