# Encoder and decoder functions 

def make_move(src, dst, flags):
    return src | (dst << 6) | (flags << 12)

def move_src(move):
    return move & 63

def move_dst(move):
    return (move >> 6) & 63 

def move_flags(move):
    return move >> 12