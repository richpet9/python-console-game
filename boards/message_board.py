import tcod as libtcodpy

from boards.board import Board

class MessageBoard(Board):
    def __init__(self, console, console_width, console_height, messages=[]):
        Board.__init__(self, console, console_width, console_height)

        self.messages = messages
    
    def render_console(self):
        # Clear after rendering
        self.console.clear(ord(' '))
        
        # For every message we have stored
        for index, message in enumerate(reversed(self.messages)):
            # If we are going past the height of the message bar (plus some padding), don't render anything
            if index >= self.console_height - 2: break

            # Make color fade the older the message is
            color = [215 - (index * 25), 215 - (index * 25), 215 - (index * 25)]

            # If this is the most recent message, make color bright white
            if index == 0: color = [255, 255, 255]

            # Draw the message
            self.console.print(1, index + 1, message, fg=color)



    def push_message(self, message):
        self.messages.append(message)

    def push_important_message(self, message):
        self.messages.append(chr(libtcodpy.COLCTRL_1) + message + chr(libtcodpy.COLCTRL_STOP))