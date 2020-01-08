class TurnActionWorker:
    def __init__(self, tiles, game_entities, player):
        self.tiles = tiles
        self.game_entities = game_entities
        self.player = player

    def do_actions_for_all(self):
        for entity in self.game_entities:
            if(len(entity.turn_actions) is not 0):
                # Execute entity turn actions some how
                for action in entity.turn_actions:
                    to_do = self.get_actions().get(action[0], None)
                    if(to_do is not None):
                        to_do(action[1])

    def get_actions(self):
        return {
            "increment_funds": self._action_increment_funds,
            "increment_research": self._action_increment_research,
            "increment_military": self._action_increment_military
        }

    def _action_increment_funds(self, amt):
        self.player.funds += amt
    
    def _action_increment_research(self, amt):
        self.player.research += amt

    def _action_increment_military(self, amt):
        self.player.military += amt

    