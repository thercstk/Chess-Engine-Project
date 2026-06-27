from constants import *
from board import Board
import attack_tables as at
import move as mv
import utils

def _is_attacked(sq, attacker, board):
    occupied = board.occupied
    return (
        at.pawn_attacks_left(1 << sq, 1 - attacker) & board.pieces[attacker][PAWNS] or
        at.pawn_attacks_right(1 << sq, 1 - attacker) & board.pieces[attacker][PAWNS] or
        at.knight_attacks(sq) & board.pieces[attacker][KNIGHTS] or
        at.bishop_attacks(sq, occupied) & board.pieces[attacker][BISHOPS] or
        at.rook_attacks(sq, occupied) & board.pieces[attacker][ROOKS] or
        at.queen_attacks(sq, occupied) & board.pieces[attacker][QUEENS] or
        at.king_attacks(sq) & board.pieces[attacker][KING]
    )

def generate_moves(board: Board) -> list:
    movelist = []

    PUSH   = [-8, 8]
    D_PUSH = [-16, 16]
    ATK_L  = [7, -9]
    ATK_R  = [9, -7]

    turn        = board.turn
    enemy_occ   = board.occupancy[1 - turn]
    occupied    = board.occupied
    passant_sq  = board.en_passant_sq

    pawns   = board.pieces[turn][PAWNS]
    knights = board.pieces[turn][KNIGHTS]
    bishops = board.pieces[turn][BISHOPS]
    rooks   = board.pieces[turn][ROOKS]
    queens  = board.pieces[turn][QUEENS]
    king    = board.pieces[turn][KING]

    castling_rights = board.castling_rights
    castling_ks = castling_rights & (1 << (2 * turn))
    castling_qs = castling_rights & (1 << (2 * turn + 1))
    ks_squares  = [(F1 | G1) & occupied, (F8 | G8) & occupied]
    qs_squares  = [(B1 | C1 | D1) & occupied, (B8 | C8 | D8) & occupied]

    # Pawn attacks generation
    d_pushes      = at.pawn_d_push(pawns, turn, occupied)
    attacks_left  = at.pawn_attacks_left(pawns, turn) & enemy_occ
    attacks_right = at.pawn_attacks_right(pawns, turn) & enemy_occ
    pushes        = at.pawn_push(pawns, turn) & ~occupied

    attacks_left_np  = attacks_left & ~RANK_8 if turn == WHITE else attacks_left & ~RANK_1
    attacks_left_p   = attacks_left &  RANK_8 if turn == WHITE else attacks_left &  RANK_1
    attacks_right_np = attacks_right & ~RANK_8 if turn == WHITE else attacks_right & ~RANK_1
    attacks_right_p  = attacks_right &  RANK_8 if turn == WHITE else attacks_right &  RANK_1

    pushes_np = pushes & ~RANK_8 if turn == WHITE else pushes & ~RANK_1
    pushes_p  = pushes &  RANK_8 if turn == WHITE else pushes &  RANK_1

    passant_left  = at.pawn_attacks_left(pawns, turn) & passant_sq
    passant_right = at.pawn_attacks_right(pawns, turn) & passant_sq
     
    while d_pushes:
        sq = utils.scan(d_pushes)
        d_pushes &= d_pushes - 1
        move = mv.make_move(sq + D_PUSH[turn], sq, double_pawn)
        movelist.append(move)
    
    while attacks_left_np:
        sq = utils.scan(attacks_left_np)
        attacks_left_np &= attacks_left_np - 1
        move = mv.make_move(sq + ATK_R[1-turn], sq, capture)
        movelist.append(move)

    while attacks_left_p:
        sq = utils.scan(attacks_left_p)
        attacks_left_p &= attacks_left_p - 1
        for flag in range(12, 16):
            move = mv.make_move(sq + ATK_R[1-turn], sq, flag)
            movelist.append(move)

    while attacks_right_np:
        sq = utils.scan(attacks_right_np)
        attacks_right_np &= attacks_right_np - 1
        move = mv.make_move(sq + ATK_L[1-turn], sq, capture)
        movelist.append(move)

    while attacks_right_p:
        sq = utils.scan(attacks_right_p)
        attacks_right_p &= attacks_right_p - 1
        for flag in range(12, 16):
            move = mv.make_move(sq + ATK_L[1-turn], sq, flag)
            movelist.append(move)

    while pushes_np:
        sq = utils.scan(pushes_np)
        pushes_np &= pushes_np - 1
        move = mv.make_move(sq + PUSH[turn], sq, quiet_move)
        movelist.append(move)

    while pushes_p:
        sq = utils.scan(pushes_p)
        pushes_p &= pushes_p - 1
        for flag in range(8, 12):
            move = mv.make_move(sq + PUSH[turn], sq, flag)
            movelist.append(move)

    if passant_left:
        sq = utils.scan(passant_left)
        move = mv.make_move(sq + ATK_R[1-turn], sq, en_passant)
        movelist.append(move)

    if passant_right:
        sq = utils.scan(passant_right)
        move = mv.make_move(sq + ATK_L[1-turn], sq, en_passant)
        movelist.append(move)

    # Knight generation
    while knights:
        sq = utils.scan(knights)
        knights &= knights - 1
        all_attacks = at.knight_attacks(sq)
        attacks_nocap = all_attacks & ~occupied
        attacks_cap = all_attacks & enemy_occ
        while attacks_nocap:
            dst = utils.scan(attacks_nocap)
            attacks_nocap &= attacks_nocap -1
            move = mv.make_move(sq, dst, quiet_move)
            movelist.append(move)
        while attacks_cap:
            dst = utils.scan(attacks_cap)
            attacks_cap &= attacks_cap -1
            move = mv.make_move(sq, dst, capture)
            movelist.append(move)
    
    # Bishop generation
    while bishops:
        sq = utils.scan(bishops)
        bishops &= bishops - 1
        all_attacks = at.bishop_attacks(sq, occupied)
        attacks_nocap = all_attacks & ~occupied
        attacks_cap = all_attacks & enemy_occ
        while attacks_nocap:
            dst = utils.scan(attacks_nocap)
            attacks_nocap &= attacks_nocap -1
            move = mv.make_move(sq, dst, quiet_move)
            movelist.append(move)
        while attacks_cap:
            dst = utils.scan(attacks_cap)
            attacks_cap &= attacks_cap -1
            move = mv.make_move(sq, dst, capture)
            movelist.append(move)
    
    # Rook generation
    while rooks:
        sq = utils.scan(rooks)
        rooks &= rooks - 1
        all_attacks = at.rook_attacks(sq, occupied)
        attacks_nocap = all_attacks & ~occupied
        attacks_cap = all_attacks & enemy_occ
        while attacks_nocap:
            dst = utils.scan(attacks_nocap)
            attacks_nocap &= attacks_nocap -1
            move = mv.make_move(sq, dst, quiet_move)
            movelist.append(move)
        while attacks_cap:
            dst = utils.scan(attacks_cap)
            attacks_cap &= attacks_cap -1
            move = mv.make_move(sq, dst, capture)
            movelist.append(move)

    # Queen generation
    while queens:
        sq = utils.scan(queens)
        queens &= queens - 1
        all_attacks = at.queen_attacks(sq, occupied)
        attacks_nocap = all_attacks & ~occupied
        attacks_cap = all_attacks & enemy_occ
        while attacks_nocap:
            dst = utils.scan(attacks_nocap)
            attacks_nocap &= attacks_nocap -1
            move = mv.make_move(sq, dst, quiet_move)
            movelist.append(move)
        while attacks_cap:
            dst = utils.scan(attacks_cap)
            attacks_cap &= attacks_cap -1
            move = mv.make_move(sq, dst, capture)
            movelist.append(move)

    # King generation
    sq = utils.scan(king)
    all_attacks = at.king_attacks(sq)
    attacks_nocap = all_attacks & ~occupied
    attacks_cap = all_attacks & enemy_occ
    while attacks_nocap:
        dst = utils.scan(attacks_nocap)
        attacks_nocap &= attacks_nocap -1
        move = mv.make_move(sq, dst, quiet_move)
        movelist.append(move)
    while attacks_cap:
        dst = utils.scan(attacks_cap)
        attacks_cap &= attacks_cap -1
        move = mv.make_move(sq, dst, capture)
        movelist.append(move)

    # Castling generation
    if turn == WHITE:
        attacked_ks = (_is_attacked(5, 1 - turn, board) or
                       _is_attacked(6, 1 - turn, board))
        attacked_qs = (_is_attacked(2, 1 - turn, board) or
                       _is_attacked(3, 1 - turn, board))
        if not attacked_ks and castling_ks and not ks_squares[turn]:
            move = mv.make_move(4, 6, king_castle)
            movelist.append(move)
        if not attacked_qs and castling_qs and not qs_squares[turn]:
            move = mv.make_move(4, 2, queen_castle)
            movelist.append(move)
    else:
        attacked_ks = (_is_attacked(61, 1 - turn, board) or
                       _is_attacked(62, 1 - turn, board))
        attacked_qs = (_is_attacked(58, 1 - turn, board) or
                       _is_attacked(59, 1 - turn, board))
        if not attacked_ks and castling_ks and not ks_squares[turn]:
            move = mv.make_move(60, 62, king_castle)
            movelist.append(move)
        if not attacked_qs and castling_qs and not qs_squares[turn]:
            move = mv.make_move(60, 58, queen_castle)
            movelist.append(move)

    return movelist