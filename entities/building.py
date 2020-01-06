from entities.entity import Entity

class Building(Entity):
    def __init__(self, x, y, char: int, fg=[255, 255, 255], bg=[0, 0, 0]):
        Entity.__init__(self, x, y, char, fg, bg)

    
