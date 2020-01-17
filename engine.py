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
from boards.research_board import ResearchBoard
from boards.loading_board import LoadingBoard
from menu_main import MainMenu
from workers.construction_worker import ConstructionWorker
from workers.turn_action__worker import TurnActionWorker
from workers.research_worker import ResearchWorker
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

        # Create main menu
        self.main_menu = MainMenu()

        # Create the construction worker
        self.construction_worker = ConstructionWorker(self.game_map.tiles, self.entities, self.player)

        # Create the turn action worker
        self.turn_action_worker = TurnActionWorker(self.game_map.tiles, self.entities, self.player)

        # Create the research worker
        self.research_worker = ResearchWorker(self.player)

        # Create the game board
        self.game_board = GameBoard(libtcodpy.console.Console(GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT), GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT, self.game_map, self.camera, self.player)

        # Create the HUD board
        self.hud_board = HUDBoard(libtcodpy.console.Console(HUD_BOARD_WIDTH, HUD_BOARD_HEIGHT), HUD_BOARD_WIDTH, HUD_BOARD_HEIGHT, self.player)

        # Create the message board
        self.message_board = MessageBoard(libtcodpy.console.Console(MESSAGE_BOARD_WIDTH, MESSAGE_BOARD_HEIGHT), MESSAGE_BOARD_WIDTH, MESSAGE_BOARD_HEIGHT)

        # Create status board
        self.status_board = StatusBoard(libtcodpy.console.Console(STATUS_BOARD_WIDTH, STATUS_BOARD_HEIGHT), STATUS_BOARD_WIDTH, STATUS_BOARD_HEIGHT, self.player)

        # Create research board
        self.research_board = ResearchBoard(libtcodpy.console.Console(GAME_BOARD_WIDTH // 3, GAME_BOARD_HEIGHT), GAME_BOARD_WIDTH // 3, GAME_BOARD_HEIGHT, self.player, self.research_worker)

        # Create the loading board
        self.loading_board = LoadingBoard(libtcodpy.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT), SCREEN_WIDTH, SCREEN_HEIGHT)

        # Create the renderer last
        self.renderer = Renderer(self)

        while True:
            # Log FPS
            # print("FPS: " + str(libtcodpy.sys_get_fps()))

            # Run everything
            self.run()

            # Render everything
            self.render()

    def run(self):
        if(self.game_state is "PLAYING" or self.game_state is "RESEARCH"):
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

        # Check if any events occured
        self.query_events()

    def render(self):
        # Render all the entities, the map, and the boards (maybe consolidate these)
        self.renderer.render_all(self.root_console, self.game_state, self.entities)
        
        # Update the console
        libtcodpy.console_flush()

    def start_new_game(self):
        # Set game state to loading
        self.game_state = "LOADING"

        # Update the loading board info
        self.loading_board.message = "Loading world"
        self.loading_board.status_message = "Creating lakes..."
        
        # Render the changes
        self.render()

        # Generate lakes, update progress and board
        self.game_map.generate_lakes()

        # Change message and bar
        self.loading_board.status_message = "Generating forests..."
        self.loading_board.progress = 0.5

        # Render changes
        self.render()

        # Generate forests
        self.game_map.generate_forests()

        # Start the game
        self.game_state = "PLAYING"

    def query_events(self):
        # Check for events
        for event in libtcodpy.event.get():
            if(event.type == "QUIT"):
                # Quit the application
                raise SystemExit()

            if(event.type == "KEYDOWN"):
                # A key was pressed, forward info to input hanlder
                escape = handle_keys(event.sym).get("escape")
                k_return = handle_keys(event.sym).get("return")
                move_player = handle_keys(event.sym).get("move_player")
                move_camera = handle_keys(event.sym).get("move_camera")
                place = handle_keys(event.sym).get("place")
                change_active = handle_keys(event.sym).get("change_active")
                research = handle_keys(event.sym).get("research")

                # Check input handler response and act accordingly
                if(escape): 
                    # End game if playing, leave research if there
                    if(self.game_state is "PLAYING"): raise SystemExit()
                    if(self.game_state is "RESEARCH"): self.game_state = "PLAYING"

                if(k_return):
                    # Start game if in main menu, increment turn if playing, do research if there
                    if(self.game_state is "MAIN_MENU"):
                        self.start_new_game()
                    elif(self.game_state is "PLAYING"):
                        # Increment turn and run turn worker
                        self.current_turn += 1
                        self.turn_action_worker.do_actions_for_all()
                    elif(self.game_state is "RESEARCH"):
                        node_to_research = self.research_board.active_node
                        worker_response = self.research_worker.research_node(node_to_research)
                        if(worker_response is True):
                            # Notify user research was successful
                            self.message_board.push_message("You researched " + node_to_research.name)
                            
                            # If available research isn't empty, "jiggle" the active board so it moves
                            if(len(self.research_worker.available_research) is not 0):
                                self.research_board.set_active_node(0)
                        else:
                            # Send error notification
                            self.message_board.push_important_message(worker_response)

                if(move_player): self.cursor.move(move_player[0], move_player[1])
                if(move_camera): self.camera.move(move_camera[0], move_camera[1])

                if(place): 
                    worker_response = self.construction_worker.construct_building(self.hud_board.active_building, self.active_tile)
                    if(worker_response is not True):
                        self.message_board.push_important_message(worker_response)
                    else:
                        self.message_board.push_message("Placing %s at (%d, %d)" % (self.hud_board.active_building["name"], self.cursor.x, self.cursor.y))
                
                if(change_active):
                    # Change active building if playing, change active research if not
                    if(self.game_state is "PLAYING"):
                        if(change_active is "down"):
                            self.hud_board.move_active_building(1)
                        else:
                            self.hud_board.move_active_building(-1)
                    elif(self.game_state is "RESEARCH"):
                        if(change_active is "down"):
                            self.research_board.move_active_node(1)
                        else:
                            self.research_board.move_active_node(-1)
                
                if(research):
                    # Open or close the research menu
                    if(self.game_state is "RESEARCH"):
                        # For future reference, this should return to PREVIOUS game state
                        self.game_state = "PLAYING"
                    else:
                        self.game_state = "RESEARCH"

def main():
    game = Engine()
    game.start_game()

if __name__ == '__main__':
    main()