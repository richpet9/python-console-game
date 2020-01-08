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