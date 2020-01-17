import tcod as libtcodpy

class Board():
    # Boards are basically libtcod consoles, with some extra fluff to work with
    def __init__(self, console_width, console_height):
        self.console = libtcodpy.console.Console(console_width, console_height)
        self.console_width = console_width
        self.console_height = console_height
