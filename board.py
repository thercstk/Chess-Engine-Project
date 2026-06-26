from constants import *
import utils

class Board:
    def __init__(self):
        self.pieces = [
            [0x000000000000FF00, 0x0000000000000042, 0x0000000000000024,
             0x0000000000000081, 0x0000000000000008, 0x0000000000000010], 
            [0x00FF000000000000, 0x4200000000000000, 0x2400000000000000, 
             0x8100000000000000, 0x0800000000000000, 0x1000000000000000]
        ]
        self.occupancy = [0x000000000000FFFF, 0xFFFF000000000000]
        self.occupied  =  0xFFFF00000000FFFF

        self.castling_rights = 15
        self.en_passant_sq = 0
        self.move_counter = 0
        self.turn = WHITE

        self.zobrist = Z_CASTLING[15]
        for turn in (0, 1):
            for i in range(6):
                bb = self.pieces[turn][i]
                while bb:
                    mask = utils.scan(bb)
                    bb &= bb - 1
                    self.zobrist ^= Z_PIECES[i][mask]