import tcod as libtcodpy

def handle_keys(key):
    if(key == libtcodpy.event.K_ESCAPE):
        return {"quit" : True}
    if(key == libtcodpy.event.K_w):
        return {"move_player" : (0, -1)}
    if(key == libtcodpy.event.K_s):
        return {"move_player" : (0, 1)}
    if(key == libtcodpy.event.K_a):
        return {"move_player" : (-1, 0)}
    if(key == libtcodpy.event.K_d):
        return {"move_player" : (1, 0)}
    if(key == libtcodpy.event.K_UP):
        return {"move_camera" : (0, 10)}
    if(key == libtcodpy.event.K_DOWN):
        return {"move_camera" : (0, -10)}
    if(key == libtcodpy.event.K_LEFT):
        return {"move_camera" : (10, 0)}
    if(key == libtcodpy.event.K_RIGHT):
        return {"move_camera" : (-10, 0)}
    if(key == libtcodpy.event.K_x):
        return {"place" : "colony"}
    if(key == libtcodpy.event.K_i):
        return {"change_building" : "up"}
    if(key == libtcodpy.event.K_k):
        return {"change_building" : "down"}

    return {}
    
