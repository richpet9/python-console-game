class ResearchTree:
    def __init__(self, root_node=None):
        self.root_node = root_node

    def display_tree(self):
        self.display_node(self.root_node)

    def display_node(self, node):
        for child in node.children:
            self.display_node(child)
        print(node.name)

    def research(self, node):
        # Check if already researched
        if(node.researched is True): return False

        # Check if every parent has been researched already
        for parent in node.parents:
            if(parent.researched is not True):
                return False

        # If every parent is researched, we can unlock this one too
        node.researched = True
        return True
