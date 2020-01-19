import tcod as libtcodpy

from boards.board import Board
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class MainMenu:
    def __init__(self):
        # Create a board for this menu
        self.board = Board(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.console = self.board.console

        self.active_option = -1

    def render(self):
        con = self.board.console
        con.clear(ord(' '))

        str_name = "PYTHON TCOD GAME"
        str_new_game = "new game"
        str_load_game = "load game"

        MENU_OPTION_WIDTH = SCREEN_WIDTH // 5

        # Print out the name of the game
        con.print((SCREEN_WIDTH // 2) - (len(str_name) // 2), (SCREEN_HEIGHT // 2) - 4, str_name)

        if(self.active_option is 0):
            # Print the new game button
            con.print((2 * MENU_OPTION_WIDTH) - (len(str_new_game) // 2), SCREEN_HEIGHT // 2, str_new_game, fg=libtcodpy.black, bg=libtcodpy.white)
            # Print the load game button
            con.print((3 * MENU_OPTION_WIDTH) - (len(str_load_game) // 2), SCREEN_HEIGHT // 2, str_load_game)
        elif(self.active_option is 1):
            # Print the new game button
            con.print((2 * MENU_OPTION_WIDTH) - (len(str_new_game) // 2), SCREEN_HEIGHT // 2, str_new_game)
            # Print the load game button
            con.print((3 * MENU_OPTION_WIDTH) - (len(str_load_game) // 2), SCREEN_HEIGHT // 2, str_load_game, fg=libtcodpy.black, bg=libtcodpy.white)
        else:
            # Print the new game button
            con.print((2 * MENU_OPTION_WIDTH) - (len(str_new_game) // 2), SCREEN_HEIGHT // 2, str_new_game)
            # Print the load game button
            con.print((3 * MENU_OPTION_WIDTH) - (len(str_load_game) // 2), SCREEN_HEIGHT // 2, str_load_game)

    def change_option(self, dir_int):
        self.active_option = (self.active_option + dir_int) % 2