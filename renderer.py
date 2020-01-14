import tcod as libtcodpy

from constants import (SCREEN_WIDTH, 
SCREEN_HEIGHT, 
HUD_BOARD_WIDTH,
HUD_BOARD_HEIGHT, 
MESSAGE_BOARD_HEIGHT, 
MESSAGE_BOARD_WIDTH, 
STATUS_BOARD_HEIGHT, 
STATUS_BOARD_WIDTH,
GAME_BOARD_WIDTH,
GAME_BOARD_HEIGHT)

class Renderer:
    def __init__(self, engine):
        self.cursor = engine.cursor
        self.camera = engine.camera
        self.game_board = engine.game_board
        self.message_board = engine.message_board
        self.hud_board = engine.hud_board
        self.status_board = engine.status_board
        self.main_menu = engine.main_menu

        self.rendered_objects = -1
    
    def render_all(self, root_console, game_state, entities):
        # Reset the debug counter
        self.rendered_objects = 0

        # Check game state
        if(game_state is "MAIN_MENU"):
            # Render the main menu
            self.main_menu.render()

            # Blit the main menu
            self.main_menu.console.blit(root_console, 0, 0, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        else:
            # Always 
            # Render game board first (the background)
            self.rendered_objects = self.game_board.render_console()

            # Render the entities
            for entity in entities:
                if(not entity.blink):
                    # Check if entity if on screen
                    if(self.entity_is_visible(entity)):
                        # This right here is important. The entities are rendered on to the GAME BOARD's console, not the root console
                        self.render_entity(self.game_board.console, entity)
                        self.rendered_objects += 1
            
            # Render the cursor
            if(not self.cursor.blink and self.entity_is_visible(self.cursor)):
                self.render_entity(self.game_board.console, self.cursor)
                self.rendered_objects += 1

            # Render the text to the message board console
            self.message_board.render_console()

            # Render the HUD
            self.hud_board.render_console()

            # Render the status board
            self.status_board.render_console()

            # Blit the individual boards into the main console
            self.message_board.console.blit(root_console, 0, SCREEN_HEIGHT - MESSAGE_BOARD_HEIGHT, 0, 0, MESSAGE_BOARD_WIDTH, MESSAGE_BOARD_HEIGHT)
            self.hud_board.console.blit(root_console, 0, 0, 0, 0, HUD_BOARD_WIDTH, HUD_BOARD_HEIGHT)
            self.status_board.console.blit(root_console, (SCREEN_WIDTH * 2) // 3, SCREEN_HEIGHT - STATUS_BOARD_HEIGHT, 0, 0, STATUS_BOARD_WIDTH, STATUS_BOARD_HEIGHT)
            self.game_board.console.blit(root_console, 0, HUD_BOARD_HEIGHT, 0, 0, GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT)
            


    def entity_is_visible(self, entity):
        return (entity.x >= self.camera.x) and (entity.x <= self.camera.x + GAME_BOARD_WIDTH) and (entity.y >= self.camera.y) and (entity.y <= self.camera.y + GAME_BOARD_HEIGHT)

    def render_entity(self, console, entity):
        console.print(entity.x - self.camera.x, entity.y - self.camera.y, chr(entity.char), fg=entity.fg, bg=entity.bg)

    def clear_entity(self, console, entity):
        console.print(entity.x - self.camera.x, entity.y - self.camera.y, ' ')


