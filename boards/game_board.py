import tcod as libtcodpy

from boards.board import Board
from constants import GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT

class GameBoard(Board):
    def __init__(self, console_width, console_height, game_map, camera, player):
        Board.__init__(self, console_width, console_height)

        self.game_map = game_map
        self.camera = camera
        self.player = player

    def render_console(self):
        # Clear the board
        self.console.clear(ord(' '))

        # Debug counter to keep track of rendered stuffs
        rendered_tiles = 0

        # Render the tiles in the map
        for y in range(self.camera.y, GAME_BOARD_HEIGHT + self.camera.y):
            for x in range(self.camera.x, GAME_BOARD_WIDTH + self.camera.x):
                self.render_tile(x, y)
                rendered_tiles += 1
        
        return rendered_tiles

    def render_tile(self, x, y):
        # Get the tile we want to render from the map
        tile = self.game_map.tiles[x][y]
        screenX = x - self.camera.x
        screenY = y - self.camera.y

        if(tile.visible is not True):
            self.console.print(screenX, screenY, ' ', bg=libtcodpy.black)
        else:
            if(tile.terrain is "forest"):
                self.console.print(screenX, screenY, 'F', [125, 160, 120], [18, 40, 15])
            elif(tile.terrain is "lake"):
                self.console.print(screenX, screenY, 'L', libtcodpy.lightest_blue, libtcodpy.desaturated_blue)
            else:
                # If the tile is not a building, or territory, or tree, render is as a green block (grass)
                self.console.print(screenX, screenY, 'G', [125, 160, 120], [25, 60, 20])

            # If this tile hasn't been render yet, mark it as officially explored
            if(tile.explored is False): tile.explored = True
        