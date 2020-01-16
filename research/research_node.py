class ResearchNode:
    def __init__(self, name=None):
        self.name = name
        self.children = []
        self.parents = []
        self.cost = 0
        self.researched = False

    def add_child(self, node):
        self.children.append(node)
        node.parents.append(self)