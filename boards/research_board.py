import tcod as libtcodpy

from boards.board import Board
from util import clamp, with_col_code

class ResearchBoard(Board):
    def __init__(self, console_width, console_height, player, research_worker):
        Board.__init__(self, console_width, console_height)
        self.player = player

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
        offset = 4

        # Display all the completed research
        for index, node in enumerate(self.completed_research):
            self.console.print(1, index + 3, node.name, fg=libtcodpy.gold)
            offset += 1

        # Display all the available research
        for index, node in enumerate(self.available_research):
            # Check if the current node is the active node
            fg_color = libtcodpy.white
            if(node is self.active_node): 
                fg_color = libtcodpy.cyan

            cost_color = 2
            if(self.player.research < node.cost): cost_color = 1

            str_research = with_col_code(cost_color, node.cost) + ' ' + node.name
            self.console.print(1, offset + index, str_research, fg=fg_color)

    def move_active_node(self, amount):
        self.active_node_index = clamp(self.active_node_index + amount, 0, len(self.available_research) - 1)
        self.active_node = self.available_research[self.active_node_index] 

    def set_active_node(self, index):
        self.active_node_index = index
        self.active_node = self.available_research[self.active_node_index]