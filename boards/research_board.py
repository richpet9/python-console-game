import tcod as libtcodpy

from boards.board import Board
from util import clamp

# TODO: when state changes to research, update the available research list

class ResearchBoard(Board):
    def __init__(self, console, console_width, console_height, research_worker):
        Board.__init__(self, console, console_width, console_height)

        self.available_research = research_worker.available_research
        self.completed_research = research_worker.completed_research
        self.active_node = self.available_research[0]
        self.active_node_index = 0
    
    def render(self):
        # Clear this console
        self.console.clear(ord(' '))

        # Helpful label yes
        self.console.print(1, 1, "RESEARCH")

        # The offset for completed research
        offset = 0

        # Display all the completed research
        for index, node in enumerate(self.completed_research):
            self.console.print(2, index + 3, node.name, fg=libtcodpy.gold)
            offset += 1

        # Display all the available research
        for index, node in enumerate(self.available_research):
            # Check if the current node is the active node
            if(node is self.active_node): 
                self.console.print(1, offset + index + 3, chr(libtcodpy.CHAR_ARROW_E), fg=libtcodpy.light_blue)

            self.console.print(2, offset + index + 3, node.name)

    def move_active_node(self, dir):
        new_index = clamp(self.active_node_index + dir, 0, len(self.available_research) - 1)
        self.active_node = self.available_research[new_index]   