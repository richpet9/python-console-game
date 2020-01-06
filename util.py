def clamp(val: int, min_val: int, max_val: int):
    if(val > max_val):
        return max_val
    else: return max(val, min_val)