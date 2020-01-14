import tcod as libtcodpy

from boards.board import Board
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class MainMenu:
    def __init__(self):
        # Create a board for this menu
        self.board = Board(libtcodpy.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT), SCREEN_WIDTH, SCREEN_HEIGHT)
        self.console = self.board.console

    def render(self):
        con = self.board.console

        str_name = "PYTHON TCOD GAME"
        con.print((SCREEN_WIDTH // 2) - (len(str_name) // 2), SCREEN_HEIGHT // 2, str_name)