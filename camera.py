from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT
from util import clamp

class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x = clamp(self.x + dx, 0, MAP_WIDTH - SCREEN_WIDTH)
        self.y = clamp(self.y + dy, 0, MAP_HEIGHT - SCREEN_HEIGHT)

# TODO:
# Fix looping character issue
# Ensure renderer isn't rendering things out of camera view
