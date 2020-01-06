import tcod as libtcodpy
import tcod.event
import time

from os import system, name
from renderer import render_all
from input_handler import handle_keys 
from map.game_map import GameMap
from camera import Camera
from entities.entity import Entity
from entities.building import Building
from workers.construction_worker import ConstructionWorker
from boards.game_board import GameBoard
from boards.message_board import MessageBoard
from boards.hud_board import HUDBoard
from boards.status_board import StatusBoard
from constants import (FONT_BITMAP_FILE,
SCREEN_WIDTH,
SCREEN_HEIGHT,
HUD_BOARD_HEIGHT,
MESSAGE_BOARD_WIDTH,
MESSAGE_BOARD_HEIGHT,
STATUS_BOARD_WIDTH,
STATUS_BOARD_HEIGHT,
MAP_WIDTH,
MAP_HEIGHT,
BLINK_DELAY)
    
def main():
    last_blink_time = -1 # ms since last blink
    player_color = libtcodpy.dark_blue

    # Set the target FPS to: 15
    libtcodpy.sys_set_fps(15)

    # Set the font
    libtcodpy.console_set_custom_font(FONT_BITMAP_FILE, libtcodpy.FONT_LAYOUT_ASCII_INROW | libtcodpy.FONT_TYPE_GRAYSCALE)

    # Set some color controllers
    libtcodpy.console_set_color_control(libtcodpy.COLCTRL_1, libtcodpy.red, libtcodpy.black)
    libtcodpy.console_set_color_control(libtcodpy.COLCTRL_2, libtcodpy.cyan, libtcodpy.black)

    # Create the root console
    root_console = libtcodpy.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'civs baby', False, libtcodpy.RENDERER_SDL2, order="F", vsync=False)

    # Create the player
    player = Entity(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2), ord('@'), libtcodpy.white, [25, 65, 45])
    
    # Create our entity container
    entities = []

    # Create our map
    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)

    # Create the camera
    camera = Camera(0, 0)

    # Create the game board
    game_board = GameBoard(libtcodpy.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT - (HUD_BOARD_HEIGHT + MESSAGE_BOARD_HEIGHT)), SCREEN_WIDTH, SCREEN_HEIGHT - (HUD_BOARD_HEIGHT + MESSAGE_BOARD_HEIGHT), game_map, camera)

    # Create the HUD board
    hud_board = HUDBoard(libtcodpy.console.Console(SCREEN_WIDTH, HUD_BOARD_HEIGHT), SCREEN_WIDTH, HUD_BOARD_HEIGHT)

    # Create the message board
    message_board = MessageBoard(libtcodpy.console.Console(MESSAGE_BOARD_WIDTH, MESSAGE_BOARD_HEIGHT), MESSAGE_BOARD_WIDTH, MESSAGE_BOARD_HEIGHT)

    # Create status board
    status_board = StatusBoard(libtcodpy.console.Console(STATUS_BOARD_WIDTH, STATUS_BOARD_HEIGHT), STATUS_BOARD_WIDTH, STATUS_BOARD_HEIGHT)

    # Create the construction worker
    construction_worker = ConstructionWorker(game_map.tiles, entities)

    while True:
        # Log FPS
        print("FPS: " + str(libtcodpy.sys_get_fps()))

        # Get the player's active tile for reference
        active_tile = game_map.tiles[player.x][player.y]

        # Get current time
        current_time = time.process_time() * 1000 # Convert to ms
        # Check if things should blink
        if(current_time - last_blink_time >= BLINK_DELAY):
            player.blink = not player.blink
            last_blink_time = current_time

        # Update entity count
        hud_board.entity_count = len(entities)

        # Send active tile to the status board for stats
        status_board.active_tile = active_tile

        # Render all the entities, the map, and the boards (maybe consolidate these)
        render_all(root_console, player, camera, entities, game_board, message_board, hud_board, status_board)

        # Update the console
        libtcodpy.console_flush()

        # Clear all the information (replace every tile with a space)
        root_console.clear(ord(' '))

        # Check for events
        for event in libtcodpy.event.get():
            if(event.type == "QUIT"):
                # Quit the application
                raise SystemExit()
            if(event.type == "KEYDOWN"):
                # A key was pressed, forward info to input hanlder
                end = handle_keys(event.sym).get("quit")
                move_player = handle_keys(event.sym).get("move_player")
                move_camera = handle_keys(event.sym).get("move_camera")
                place = handle_keys(event.sym).get("place")
                change_building = handle_keys(event.sym).get("change_building")

                # Check input handler response and act accordingly
                if(end): raise SystemExit()
                if(move_player): player.move(move_player[0], move_player[1])
                if(move_camera): camera.move(move_camera[0], move_camera[1])
                if(place): 
                    # TODO: The 0 in the below line is the UID of the building, this info will
                    #  be relayed from an interface handler
                    if(construction_worker.construct_building(hud_board.active_building, active_tile)):
                        message_board.push_message("Placing %s at (%d, %d)" % (hud_board.active_building["name"], player.x, player.y))
                    else:
                        message_board.push_important_message("A building is already located at [%d, %d]" % (player.x, player.y))
                if(change_building):
                    if(change_building == "down"):
                        hud_board.move_active_building(1)
                    else:
                        hud_board.move_active_building(-1)


if __name__ == '__main__':
     main()