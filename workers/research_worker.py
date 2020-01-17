import json

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
    with open("data/research.json") as file:
        data = json.load(file)
    
    if(data):
        loaded_nodes = [ResearchNode(0, "Empiricism")]
        unloaded_nodes = []

        for research_node in data:
            if(research_node["requirements"] is None):
                new_node = ResearchNode(research_node["RID"], research_node["name"])
                loaded_nodes[0].add_child(new_node)
                loaded_nodes.append(new_node)
            else:
                # This node has requirements
                new_node = ResearchNode(research_node["RID"], research_node["name"])
                loaded = False
                for req_id in research_node["requirements"]:
                    for node in loaded_nodes:
                        if(req_id is node.rid):
                            node.add_child(new_node)
                            loaded_nodes.append(new_node)
                            loaded = True
                
                if(not loaded):
                    unloaded_nodes.append(new_node)
                    print("Couldn't load research node (%s) (%d). Ensure all requirements are loaded before this node."%(new_node.name, new_node.rid))
                


    return ResearchTree(loaded_nodes[0])