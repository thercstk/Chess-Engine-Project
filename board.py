class BB:
    # Static Helper Bitboards
    white_squares = 0x55AA55AA55AA55AA
    black_squares = 0xAA55AA55AA55AA55
    full          = 0xFFFFFFFFFFFFFFFF
    empty         = 0x0000000000000000
    # File and Ranks
    file_a        = 0x0101010101010101
    file_b        = 0x0202020202020202
    file_c        = 0x0404040404040404
    file_d        = 0x0808080808080808  
    file_e        = 0x1010101010101010
    file_f        = 0x2020202020202020
    file_g        = 0x4040404040404040
    file_h        = 0x8080808080808080
    rank_1        = 0x00000000000000FF
    rank_2        = 0x000000000000FF00
    rank_3        = 0x0000000000FF0000
    rank_4        = 0x00000000FF000000
    rank_5        = 0x000000FF00000000
    rank_6        = 0x0000FF0000000000
    rank_7        = 0x00FF000000000000
    rank_8        = 0xFF00000000000000
    
    def __init__(self) -> None:
        # White Pieces
        self.white_pawns   = 0x000000000000FF00
        self.white_knights = 0x0000000000000042
        self.white_bishops = 0x0000000000000024
        self.white_rooks   = 0x0000000000000081
        self.white_queens  = 0x0000000000000008
        self.white_king    = 0x0000000000000010
        # Black Pieces
        self.black_pawns   = 0x00FF000000000000
        self.black_knights = 0x4200000000000000
        self.black_bishops = 0x2400000000000000
        self.black_rooks   = 0x8100000000000000
        self.black_queens  = 0x0800000000000000
        self.black_king    = 0x1000000000000000
        # Helper Bitboards
        self.white_pieces  = 0x000000000000FFFF
        self.black_pieces  = 0xFFFF000000000000
        self.occupied      = 0xFFFF00000000FFFF
        self.non_occupied  = self.full ^ self.occupied

    def print_board(self):
        board = [""] * 64
        for i in range(64):
            mask = 1 << i
            if self.white_pawns & mask:
                board[i] = 'P'
            elif self.white_knights & mask:
                board[i] = 'N'
            elif self.white_bishops & mask:
                board[i] = 'B'
            elif self.white_rooks & mask:
                board[i] = 'R'
            elif self.white_queens & mask:
                board[i] = 'Q'
            elif self.white_king & mask:
                board[i] = 'K'
            elif self.black_pawns & mask:
                board[i] = 'p'
            elif self.black_knights & mask:
                board[i] = 'n'
            elif self.black_bishops & mask:
                board[i] = 'b'
            elif self.black_rooks & mask:
                board[i] = 'r'
            elif self.black_queens & mask:
                board[i] = 'q'
            elif self.black_king & mask:
                board[i] = 'k'
            else:
                board[i] = '.'
        
        for rank in range(7, -1, -1):
            print(' '.join(board[rank*8:(rank+1)*8]))
        