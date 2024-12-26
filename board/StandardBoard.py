from typing import List, Tuple
from board.Board import *

class StandardBoard(Board):
    def __init__(self):
        """
        """
        self.force_capture = False
        super().__init__()

    def enable_force_capture(self):
        if self.num_turns == 0:
            self.force_capture = True

    def disable_force_capture(self):
        if self.num_turns == 0:
            self.force_capture = False

    # @override
    def get_piece_capture_moves(self, piece: Piece):
        """
        """
        row = piece.row
        col = piece.col
        moves = {}
        can_capture = 0
        if piece.is_king or piece.player == PlayerId.ONE:
            if self.check_in_bounds(row - 1, col - 1) and self.board[row - 1][col - 1] != -1:
                neighbor_piece = self.board[row - 1][col - 1]
                if neighbor_piece.player != piece.player:
                    if self.check_in_bounds(row - 2, col - 2) and self.board[row - 2][col - 2] == -1:
                        moves[(row - 2, col - 2)] = neighbor_piece
                        can_capture = True
            if self.check_in_bounds(row - 1, col + 1) and self.board[row - 1][col + 1] != -1:
                neighbor_piece = self.board[row - 1][col + 1]
                if neighbor_piece.player != piece.player:
                    if self.check_in_bounds(row - 2, col + 2) and self.board[row - 2][col + 2] == -1:
                        moves[(row - 2, col + 2)] = neighbor_piece
                        can_capture = True
        if piece.is_king or piece.player == PlayerId.TWO:
            if self.check_in_bounds(row + 1, col - 1) and self.board[row + 1][col - 1] != -1:
                neighbor_piece = self.board[row + 1][col - 1]
                if neighbor_piece.player != piece.player:
                    if self.check_in_bounds(row + 2, col - 2) and self.board[row + 2][col - 2] == -1:
                        moves[(row + 2, col - 2)] = neighbor_piece
                        can_capture = True
            if self.check_in_bounds(row + 1, col + 1) and self.board[row + 1][col + 1] != -1:
                neighbor_piece = self.board[row + 1][col + 1]
                if neighbor_piece.player != piece.player:                
                    if self.check_in_bounds(row + 2, col + 2) and self.board[row + 2][col + 2] == -1:
                        moves[(row + 2, col + 2)] = neighbor_piece
                        can_capture = True
        return moves, can_capture

    # @override
    def get_piece_moves(self, piece: Piece):
        """
        """
        moves = {}
        can_capture = False
        row = piece.row
        col = piece.col
        if row != -1 or col != -1:
            moves, can_capture = self.get_piece_capture_moves(piece)
            if not self.force_capture or (self.force_capture and not can_capture):
                if piece.is_king or piece.player == PlayerId.ONE:
                    if self.check_in_bounds(row - 1, col - 1) and self.board[row - 1][col - 1] == -1:
                        moves[(row - 1, col - 1)] = None
                    if self.check_in_bounds(row - 1, col + 1) and self.board[row - 1][col + 1] == -1:
                        moves[(row - 1, col + 1)] = None
                if piece.is_king or piece.player == PlayerId.TWO:
                    if self.check_in_bounds(row + 1, col - 1) and self.board[row + 1][col - 1] == -1:
                        moves[(row + 1, col - 1)] = None
                    if self.check_in_bounds(row + 1, col + 1) and self.board[row + 1][col + 1] == -1:
                        moves[(row + 1, col + 1)] = None
        return moves, can_capture

    # @override
    def get_all_moves(self):
        """
        """
        capture_move = False
        move_dict = {}
        print("TURN", self.turn)
        player = self.players[self.turn]
        for piece in player.pieces:
            moves, can_capture = self.get_piece_moves(piece)
            piece_hash = (piece.row, piece.col)
            
            if self.force_capture:
                if can_capture:
                    if not capture_move:
                        move_dict = {}
                        capture_move= True
                    move_dict[piece_hash] = moves
                elif not capture_move and len(moves) > 0:
                    move_dict[piece_hash] = moves
            else:
                move_dict[piece_hash] = moves
        return move_dict
