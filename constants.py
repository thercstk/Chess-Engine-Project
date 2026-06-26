import random

# Definitions

PAWNS, KNIGHTS, BISHOPS, ROOKS, QUEENS, KING = range(6)

WHITE = 0
BLACK = 1

# Flags for Move Generation

quiet_move      = 0b0000 # 0
double_pawn     = 0b0001 # 1
king_castle     = 0b0010 # 2
queen_castle    = 0b0011 # 3
capture         = 0b0100 # 4
en_passant      = 0b0101 # 5
knight_prom     = 0b1000 # 8
bishop_prom     = 0b1001 # 9
rook_prom       = 0b1010 # 10
queen_prom      = 0b1011 # 11
knight_prom_cap = 0b1100 # 12
bishop_prom_cap = 0b1101 # 13
rook_prom_cap   = 0b1110 # 14
queen_prom_cap  = 0b1111 # 15

# Individual Squares

A1, B1, C1, D1, E1, F1, G1, H1 = (1 << i for i in range(8))
A2, B2, C2, D2, E2, F2, G2, H2 = (1 << i for i in range(8, 16))
A3, B3, C3, D3, E3, F3, G3, H3 = (1 << i for i in range(16, 24))
A4, B4, C4, D4, E4, F4, G4, H4 = (1 << i for i in range(24, 32))
A5, B5, C5, D5, E5, F5, G5, H5 = (1 << i for i in range(32, 40))
A6, B6, C6, D6, E6, F6, G6, H6 = (1 << i for i in range(40, 48))
A7, B7, C7, D7, E7, F7, G7, H7 = (1 << i for i in range(48, 56))
A8, B8, C8, D8, E8, F8, G8, H8 = (1 << i for i in range(56, 64))

# Files and Ranks

FILE_A = 0x0101010101010101
FILE_B = 0x0202020202020202
FILE_C = 0x0404040404040404
FILE_D = 0x0808080808080808
FILE_E = 0x1010101010101010
FILE_F = 0x2020202020202020
FILE_G = 0x4040404040404040
FILE_H = 0x8080808080808080
RANK_1 = 0x00000000000000FF
RANK_2 = 0x000000000000FF00
RANK_3 = 0x0000000000FF0000
RANK_4 = 0x00000000FF000000
RANK_5 = 0x000000FF00000000
RANK_6 = 0x0000FF0000000000
RANK_7 = 0x00FF000000000000
RANK_8 = 0xFF00000000000000

# Helper Bitboards

WHITE_SQUARES = 0x55AA55AA55AA55AA
BLACK_SQUARES = 0xAA55AA55AA55AA55
FULL_BOARD    = 0xFFFFFFFFFFFFFFFF
EMPTY_BOARD   = 0x0000000000000000
BOARD_EDGE    = RANK_1 | RANK_8 | FILE_A | FILE_H

# Zobrist Hashing

Z_PIECES     = [[random.getrandbits(64) for _ in range(64)] for _ in range(12)]
Z_CASTLING   = [random.getrandbits(64) for _ in range(16)]
Z_EN_PASSANT = [random.getrandbits(64) for _ in range(8)]
Z_SIDE       = random.getrandbits(64)

# De Brujin Multiplication

DEBRUJIN64  = 0x03F79D71B4CA8B09

DEBRUJIN_ID = [
    0,  1, 48,  2, 57, 49, 28,  3,
   61, 58, 50, 42, 38, 29, 17,  4,
   62, 55, 59, 36, 53, 51, 43, 22,
   45, 39, 33, 30, 24, 18, 12,  5,
   63, 47, 56, 27, 60, 41, 37, 16,
   54, 35, 52, 21, 44, 32, 23, 11,
   46, 26, 40, 15, 34, 20, 31, 10,
   25, 14, 19,  9, 13,  8,  7,  6
]