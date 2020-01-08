from world.tile import Tile
from tcod import (
    COLCTRL_1,
    COLCTRL_2,
    COLCTRL_3,
    COLCTRL_4,
    COLCTRL_5,
    COLCTRL_BACK_RGB,
    COLCTRL_FORE_RGB,
    COLCTRL_STOP
)
from constants import MAP_WIDTH, MAP_HEIGHT

def clamp(val: int, min_val: int, max_val: int):
    if(val > max_val):
        return max_val
    else: return max(val, min_val)

def with_col_code(col_code, string):
    if(col_code == 1):
        return chr(COLCTRL_1) + string + chr(COLCTRL_STOP)
    if(col_code == 2):
        return chr(COLCTRL_2) + string + chr(COLCTRL_STOP)
    if(col_code == 3):
        return chr(COLCTRL_3) + string + chr(COLCTRL_STOP)
    if(col_code == 4):
        return chr(COLCTRL_4) + string + chr(COLCTRL_STOP)
    if(col_code == 5):
        return chr(COLCTRL_5) + string + chr(COLCTRL_STOP)
    
    return string

def get_tile_neighbors(tile):
    if(type(tile) is not Tile): 
        raise TypeError("Invalid arguement for get_tile_neighbors: " + type(tile) + " expected " + type(Tile))

    res = []

    for y in range(3):
        for x in range(3):
            new_x = (tile.x - 1) + x
            new_y = (tile.y - 1) + y

            if(new_x < 0 or new_x > MAP_WIDTH - 1): continue
            if(new_y < 0 or new_y > MAP_HEIGHT - 1): continue
            if(new_x == tile.x and new_y == tile.y): continue

            res.append((new_x, new_y))

    return res