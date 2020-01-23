import tcod as libtcodpy

from boards.board import Board
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class MainMenu:
    def __init__(self):
        # Create a board for this menu
        self.board = Board(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.console = self.board.console

        self.active_option = 0
        self.options = [
            "new game",
            "load game"
        ]

    def render(self):
        con = self.board.console
        con.clear(ord(' '))

        str_name = "PYTHON TCOD GAME"

        MENU_OPTION_WIDTH = SCREEN_WIDTH // 5

        # Print out the name of the game
        con.print((SCREEN_WIDTH // 2) - (len(str_name) // 2), (SCREEN_HEIGHT // 2) - 4, str_name)

        # Print out escape info
        con.print((SCREEN_WIDTH // 2) - (len(str_name) // 2), (SCREEN_HEIGHT // 2) - 4, str_name)

        # Print out options
        for index, option in enumerate(self.options):
            x = ((2 + index) * MENU_OPTION_WIDTH) - (len(option) // 2)
            y = SCREEN_HEIGHT // 2
            fg_color = libtcodpy.black if self.active_option is index else libtcodpy.white
            bg_color = libtcodpy.white if self.active_option is index else libtcodpy.black
            con.print(x, y, option, fg=fg_color, bg=bg_color)

    def change_option(self, dir_int):
        self.active_option = (self.active_option + dir_int) % 2