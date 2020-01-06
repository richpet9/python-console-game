import tcod as libtcodpy

from constants import (SCREEN_WIDTH, 
SCREEN_HEIGHT, 
HUD_BOARD_HEIGHT, 
MESSAGE_BOARD_HEIGHT, 
MESSAGE_BOARD_WIDTH, 
STATUS_BOARD_HEIGHT, 
STATUS_BOARD_WIDTH)

def render_all(root_console, player, entities, game_board, message_board, hud_board, status_board):
    # Always render game board first (the background)
    game_board.render_console()

    # Render the entities
    for entity in entities:
        if not entity.blink:
            # This right here is important. The entities are rendered on to the GAME BOARD's
            # console, not the root console
            render_entity(game_board.console, entity)

    # Render the player
    if not player.blink:
        render_entity(game_board.console, player)
    
    # Render the text to the message board console
    message_board.render_console()
    # Blit the message board console to the root
    message_board.console.blit(root_console, 0, SCREEN_HEIGHT - MESSAGE_BOARD_HEIGHT, 0, 0, MESSAGE_BOARD_WIDTH, MESSAGE_BOARD_HEIGHT)

    # Render the HUD
    hud_board.render_console()

    # Render the status board
    status_board.render_console()

    hud_board.console.blit(root_console, 0, 0, 0, 0, hud_board.console_width, hud_board.console_height)
    status_board.console.blit(root_console, int((SCREEN_WIDTH * 2) / 3), SCREEN_HEIGHT - STATUS_BOARD_HEIGHT, 0, 0, STATUS_BOARD_WIDTH, STATUS_BOARD_HEIGHT)
    game_board.console.blit(root_console, 0, HUD_BOARD_HEIGHT, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - (HUD_BOARD_HEIGHT + MESSAGE_BOARD_HEIGHT))
    
    # Blit the console
    root_console.blit(root_console, 0, 0, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

def render_entity(console, entity):
    console.print(entity.x, entity.y, chr(entity.char), fg=entity.fg, bg=entity.bg)

def clear_entity(console, entity):
    console.print(entity.x, entity.y, ' ')

