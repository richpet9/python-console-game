from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT

class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

# TODO:
# Clean up the renderer class, make it a class
# Make sure camera directions are proper
# Fix looping character issue
# Ensure renderer isn't rendering things out of camera view
