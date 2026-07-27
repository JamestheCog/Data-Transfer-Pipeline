def to_mb(raw_size: float) -> float:
    '''
    Converts raw byte values to Mbs
    '''
    return raw_size / 1024**2 if raw_size else 0