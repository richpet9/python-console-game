import tcod as libtcodpy

from boards.board import Board
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class LoadingBoard(Board):
    def __init__(self, console_width, console_height):
        Board.__init__(self, console_width, console_height)

        self.message = "Loading..."
        self.status_message = ' '
        self.progress = 0

    def render_console(self):
        # Clear the console first
        self.console.clear(ord(' '))

        # Draw the message
        self.console.print((SCREEN_WIDTH // 2) - (len(self.message) // 2), (SCREEN_HEIGHT // 2) - 4, self.message)

        # Draw the status message
        self.console.print((SCREEN_WIDTH // 2) - (len(self.status_message) // 2), (SCREEN_HEIGHT // 2) - 2, self.status_message)

        # Draw the loading bar
        BAR_WIDTH = 25
        for i in range(BAR_WIDTH):
            color = libtcodpy.dark_gray
            if(i / BAR_WIDTH <= self.progress):
                color = libtcodpy.lighter_gray
            self.console.print((SCREEN_WIDTH // 2) - (BAR_WIDTH // 2) + i, SCREEN_HEIGHT // 2, chr(libtcodpy.CHAR_HLINE), fg=color)
        