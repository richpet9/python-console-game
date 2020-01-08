from entities.entity import Entity
from workers.turn_action__worker import TurnActionWorker

class Building(Entity):
    def __init__(self, x, y, char: int, fg=[255, 255, 255], bg=[0, 0, 0]):
        Entity.__init__(self, x, y, char, fg, bg)

        self.turn_actions = []

    def add_turn_action(self, action, value):
        self.turn_actions.append((action, value))
            
    
