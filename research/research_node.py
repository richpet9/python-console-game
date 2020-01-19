class ResearchNode:
    def __init__(self, rid, name=None, cost=0):
        self.rid = rid
        self.name = name
        self.cost = cost

        self.children = []
        self.parents = []
        self.researched = False

    def add_child(self, node):
        self.children.append(node)
        node.parents.append(self)
