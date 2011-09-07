def get_int_or_none(d, key):
    x = d.get(key, None)
    
    if x is not None:
        return int(x)