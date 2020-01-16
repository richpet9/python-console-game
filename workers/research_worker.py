from research.research_tree import ResearchTree
from research.research_node import ResearchNode

class ResearchWorker:
    def __init__(self, player):
        self.player = player
        self.research_tree = read_in_research_tree()
        self.available_research = [self.research_tree.root_node]
        self.completed_research = []
    
    def research_node(self, node):
        if(node in self.available_research):
            # Mark this node as researched
            node.researched = True
            # Add it to the completed list
            self.completed_research.append(node)
            # Remove it from the available list
            self.available_research.remove(node)

            # Go through every node child
            for child in node.children:
                is_available = True

                # If any parent is not researched, this child is not available yet
                for parent in child.parents:
                    if(parent.researched is not True):
                        is_available = False

                # Add this child to the available list, since it was unlocked
                if(is_available): self.available_research.append(child)

def read_in_research_tree():
    # For debugging
    node1 = ResearchNode("Happy fun animals")

    node2 = ResearchNode("Neato plants in dirt")

    node3 = ResearchNode("Spinny wheels")

    node4 = ResearchNode("Internal Combustion Engine")

    node1.add_child(node2)
    node1.add_child(node3)

    node3.add_child(node4)
    node2.add_child(node4)

    return ResearchTree(node1)