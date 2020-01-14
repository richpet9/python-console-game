import tcod as libtcodpy
import tcod.event
import time

from os import system, name
from renderer import Renderer
from input_handler import handle_keys 
from camera import Camera
from player import Player
from world.game_map import GameMap
from entities.entity import Entity
from entities.building import Building
from boards.game_board import GameBoard
from boards.message_board import MessageBoard
from boards.hud_board import HUDBoard
from boards.status_board import StatusBoard
from menu_main import MainMenu
from workers.construction_worker import ConstructionWorker
from workers.turn_action__worker import TurnActionWorker
from constants import (
    FONT_BITMAP_FILE,
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
    BLINK_DELAY
)

class Engine:
    def __init__(self):
        # Set the target FPS to: 15
        libtcodpy.sys_set_fps(15)

        # Set the font
        libtcodpy.console_set_custom_font(FONT_BITMAP_FILE, libtcodpy.FONT_LAYOUT_TCOD | libtcodpy.FONT_TYPE_GRAYSCALE)

        # Set some color controllers
        libtcodpy.console_set_color_control(libtcodpy.COLCTRL_1, libtcodpy.red, libtcodpy.black)
        libtcodpy.console_set_color_control(libtcodpy.COLCTRL_2, libtcodpy.cyan, libtcodpy.black)
        libtcodpy.console_set_color_control(libtcodpy.COLCTRL_3, libtcodpy.yellow, libtcodpy.black)
        libtcodpy.console_set_color_control(libtcodpy.COLCTRL_4, libtcodpy.red, libtcodpy.black)
        libtcodpy.console_set_color_control(libtcodpy.COLCTRL_5, libtcodpy.orange, libtcodpy.black)

        # Create the root console
        self.root_console = libtcodpy.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Python TCOD Game', False, libtcodpy.RENDERER_SDL2, order="F", vsync=False)

        # Create our instance variables
        self.game_state = "MAIN_MENU"
        self.last_blink_time = -1  # ms since last blink
        self.current_time = 0
        self.current_turn = 0
        self.active_tile = None

    def start_game(self):
        # Create the camera
        self.camera = Camera(0, 0)

        # Create the player's civilization
        self.player = Player("Richie's civ", 0, libtcodpy.blue)

        # Create the cursor
        self.cursor = Entity(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, ord('@'), libtcodpy.white, [25, 65, 45])
        
        # Create our entity container
        self.entities = []

        # Create our map
        self.game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)

        # Create the game board
        self.game_board = GameBoard(libtcodpy.console.Console(GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT), GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT, self.game_map, self.camera, self.player)

        # Create the HUD board
        self.hud_board = HUDBoard(libtcodpy.console.Console(HUD_BOARD_WIDTH, HUD_BOARD_HEIGHT), HUD_BOARD_WIDTH, HUD_BOARD_HEIGHT, self.player)

        # Create the message board
        self.message_board = MessageBoard(libtcodpy.console.Console(MESSAGE_BOARD_WIDTH, MESSAGE_BOARD_HEIGHT), MESSAGE_BOARD_WIDTH, MESSAGE_BOARD_HEIGHT)

        # Create status board
        self.status_board = StatusBoard(libtcodpy.console.Console(STATUS_BOARD_WIDTH, STATUS_BOARD_HEIGHT), STATUS_BOARD_WIDTH, STATUS_BOARD_HEIGHT, self.player)

        # Create main menu
        self.main_menu = MainMenu()

        # Create the construction worker
        self.construction_worker = ConstructionWorker(self.game_map.tiles, self.entities, self.player)

        # Create the turn action worker
        self.turn_action_worker = TurnActionWorker(self.game_map.tiles, self.entities, self.player)

        # Create the renderer last
        self.renderer = Renderer(self)

        while True:
            # Log FPS
            print("FPS: " + str(libtcodpy.sys_get_fps()))

            # Run everything
            self.run()

    def run(self):
        if(self.game_state is "PLAYING"):
            # Get the self.cursor's active tile for reference
            self.active_tile = self.game_map.tiles[self.cursor.x][self.cursor.y]

            # Get current time
            self.current_time = time.process_time() * 1000 # Convert to ms

            # Check if cursor should blink
            if(self.current_time - self.last_blink_time >= BLINK_DELAY):
                self.cursor.blink = not self.cursor.blink
                self.last_blink_time = self.current_time

            # Update HUD info 
            self.hud_board.entity_count = len(self.entities)
            self.hud_board.rendered_objects = self.renderer.rendered_objects
            self.hud_board.current_turn = self.current_turn

            # Send active tile to the status board for stats
            self.status_board.active_tile = self.active_tile

        # Render all the entities, the map, and the boards (maybe consolidate these)
        self.renderer.render_all(self.root_console, self.game_state, self.entities)

        # Update the console
        libtcodpy.console_flush()

        # Clear all the information (replace every tile with a space)
        self.root_console.clear(ord(' '))

        # Check if any events occured
        self.query_events()

    def start_new_game(self):
        self.game_state = "PLAYING"
        self.game_map.generate_tiles()

    def query_events(self):
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
                    if(self.game_state is "MAIN_MENU"):
                        self.start_new_game()
                    else:
                        # Increment turn and run turn worker
                        self.current_turn += 1
                        self.turn_action_worker.do_actions_for_all()
                if(move_player): self.cursor.move(move_player[0], move_player[1])
                if(move_camera): self.camera.move(move_camera[0], move_camera[1])
                if(place): 
                    worker_response = self.construction_worker.construct_building(self.hud_board.active_building, self.active_tile)
                    if(worker_response is not True):
                        self.message_board.push_important_message(worker_response)
                    else:
                        self.message_board.push_message("Placing %s at (%d, %d)" % (self.hud_board.active_building["name"], self.cursor.x, self.cursor.y))
                if(change_building):
                    if(change_building == "down"):
                        self.hud_board.move_active_building(1)
                    else:
                        self.hud_board.move_active_building(-1)

def main():
    game = Engine()
    game.start_game()

if __name__ == '__main__':
    main()