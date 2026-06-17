from constants import *

def scan(bb: int) -> int:
    mask = bb & -bb
    return DEBRUJIN_ID[((mask * DEBRUJIN64) & FULL_BOARD) >> 58]

def print_bb(bb: int):
    board = ['0'] * 64
    for i in range(64):
        if 1 << i & bb != 0:
            board[i] = '1'
    for i in range(7, -1, -1):
        print('['+' '.join(board[i*8:(i+1)*8])+']')