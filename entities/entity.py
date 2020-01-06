class Entity:
    def __init__(self, x, y, char, fg=[255, 255, 255], bg=[0, 0, 0], blink=False):
        self.x = x
        self.y = y
        self.char = char
        self.fg = fg
        self.bg = bg
        self.blink = blink

    def move(self, dx, dy):
        self.x += dx
        self.y += dy