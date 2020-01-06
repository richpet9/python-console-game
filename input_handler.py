import tcod as libtcodpy

def handle_keys(key):
    if(key == libtcodpy.event.K_ESCAPE):
        return {"quit" : True}
    if(key == libtcodpy.event.K_w or key == libtcodpy.event.K_UP):
        return {"move" : (0, -1)}
    if(key == libtcodpy.event.K_s or key == libtcodpy.event.K_DOWN):
        return {"move" : (0, 1)}
    if(key == libtcodpy.event.K_a or key == libtcodpy.event.K_LEFT):
        return {"move" : (-1, 0)}
    if(key == libtcodpy.event.K_d or key == libtcodpy.event.K_RIGHT):
        return {"move" : (1, 0)}
    if(key == libtcodpy.event.K_x):
        return {"place" : "colony"}
    if(key == libtcodpy.event.K_i):
        return {"change_building" : "up"}
    if(key == libtcodpy.event.K_k):
        return {"change_building" : "down"}

    return {}
    