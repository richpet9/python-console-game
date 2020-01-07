import tcod as libtcodpy
import tcod.event
import time

from os import system, name
from renderer import Renderer
from input_handler import handle_keys 
from camera import Camera
from player import Player
from map.game_map import GameMap
from entities.entity import Entity
from entities.building import Building
from boards.game_board import GameBoard
from boards.message_board import MessageBoard
from boards.hud_board import HUDBoard
from boards.status_board import StatusBoard
from workers.construction_worker import ConstructionWorker
from workers.turn_action__worker import TurnActionWorker
from constants import (FONT_BITMAP_FILE,
SCREEN_WIDTH,
SCREEN_HEIGHT,
MAP_WIDTH,
MAP_HEIGHT,
HUD_BOARD_WIDTH,
HUD_BOARD_HEIGHT,
MESSAGE_BOARD_WIDTH,
MESSAGE_BOARD_HEIGHT,
STATUS_BOARD_WIDTH,
STATUS_BOARD_HEIGHT,
GAME_BOARD_WIDTH,
GAME_BOARD_HEIGHT,
BLINK_DELAY)
    
def main():
    last_blink_time = -1 # ms since last blink
    player_color = libtcodpy.dark_blue
    current_turn = 0

    # Set the target FPS to: 15
    libtcodpy.sys_set_fps(15)

    # Set the font
    libtcodpy.console_set_custom_font(FONT_BITMAP_FILE, libtcodpy.FONT_LAYOUT_ASCII_INROW | libtcodpy.FONT_TYPE_GRAYSCALE)

    # Set some color controllers
    libtcodpy.console_set_color_control(libtcodpy.COLCTRL_1, libtcodpy.red, libtcodpy.black)
    libtcodpy.console_set_color_control(libtcodpy.COLCTRL_2, libtcodpy.cyan, libtcodpy.black)
    libtcodpy.console_set_color_control(libtcodpy.COLCTRL_3, libtcodpy.yellow, libtcodpy.black)
    libtcodpy.console_set_color_control(libtcodpy.COLCTRL_4, libtcodpy.red, libtcodpy.black)
    libtcodpy.console_set_color_control(libtcodpy.COLCTRL_5, libtcodpy.orange, libtcodpy.black)

    # Create the root console
    root_console = libtcodpy.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'civs baby', False, libtcodpy.RENDERER_SDL2, order="F", vsync=False)

    # Create the camera
    camera = Camera(0, 0)

    # -- The below occurs when we click play --

    # Create the player's civilization
    player = Player("Richie's civ", 0, libtcodpy.blue)

    # Create the cursor
    cursor = Entity(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, ord('@'), libtcodpy.white, [25, 65, 45])
    
    # Create our entity container
    entities = []

    # Create our map
    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)

    # Create the game board
    game_board = GameBoard(libtcodpy.console.Console(GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT), GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT, game_map, camera)

    # Create the HUD board
    hud_board = HUDBoard(libtcodpy.console.Console(HUD_BOARD_WIDTH, HUD_BOARD_HEIGHT), HUD_BOARD_WIDTH, HUD_BOARD_HEIGHT, player)

    # Create the message board
    message_board = MessageBoard(libtcodpy.console.Console(MESSAGE_BOARD_WIDTH, MESSAGE_BOARD_HEIGHT), MESSAGE_BOARD_WIDTH, MESSAGE_BOARD_HEIGHT)

    # Create status board
    status_board = StatusBoard(libtcodpy.console.Console(STATUS_BOARD_WIDTH, STATUS_BOARD_HEIGHT), STATUS_BOARD_WIDTH, STATUS_BOARD_HEIGHT)

    # Create the construction worker
    construction_worker = ConstructionWorker(game_map.tiles, entities, player)

    # Create the turn action worker
    turn_action_worker = TurnActionWorker(game_map.tiles, entities, player)

    # Create the renderer last
    renderer = Renderer(cursor, camera, game_board, message_board, hud_board, status_board)

    while True:
        # Log FPS
        print("FPS: " + str(libtcodpy.sys_get_fps()))

        # Get the cursor's active tile for reference
        active_tile = game_map.tiles[cursor.x][cursor.y]

        # Get current time
        current_time = time.process_time() * 1000 # Convert to ms
        # Check if things should blink
        if(current_time - last_blink_time >= BLINK_DELAY):
            cursor.blink = not cursor.blink
            last_blink_time = current_time

        # Update HUD info 
        # TODO: Make engine a class and pass it to hud to remove these
        hud_board.entity_count = len(entities)
        hud_board.rendered_objects = renderer.rendered_objects
        hud_board.current_turn = current_turn

        # Send active tile to the status board for stats
        status_board.active_tile = active_tile

        # Render all the entities, the map, and the boards (maybe consolidate these)
        renderer.render_all(root_console, entities)

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
                end_game = handle_keys(event.sym).get("exit")
                end_turn = handle_keys(event.sym).get("end_turn")
                move_player = handle_keys(event.sym).get("move_player")
                move_camera = handle_keys(event.sym).get("move_camera")
                place = handle_keys(event.sym).get("place")
                change_building = handle_keys(event.sym).get("change_building")

                # Check input handler response and act accordingly
                if(end_game): raise SystemExit()
                if(end_turn):
                    # Increment turn and run turn worker
                    current_turn += 1
                    turn_action_worker.do_actions_for_all()
                if(move_player): cursor.move(move_player[0], move_player[1])
                if(move_camera): camera.move(move_camera[0], move_camera[1])
                if(place): 
                    worker_response = construction_worker.construct_building(hud_board.active_building, active_tile)
                    if(worker_response is not True):
                        message_board.push_important_message(worker_response)
                    else:
                        message_board.push_message("Placing %s at (%d, %d)" % (hud_board.active_building["name"], cursor.x, cursor.y))
                if(change_building):
                    if(change_building == "down"):
                        hud_board.move_active_building(1)
                    else:
                        hud_board.move_active_building(-1)



if __name__ == '__main__':
     main()