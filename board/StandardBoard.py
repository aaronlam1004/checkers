from typing import List, Tuple
from board.Board import *

class StandardBoard(Board):
    def __init__(self, force_capture: bool = False):
        """
        """
        self.force_capture = force_capture
        super().__init__(size=8)

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
            if len(moves) == 0:
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
        capture = False
        move_dict = {}
        print("TURN", self.turn)
        player = self.players[self.turn]
        for piece in player.pieces:
            moves, can_capture = self.get_piece_moves(piece)
            piece_hash = (piece.row, piece.col)

            # TODO: add not force capture
            if self.force_capture:
                if can_capture:
                    if not capture:
                        move_dict = {}
                        can_capture_flag= True
                    move_dict[piece_hash] = moves
                elif not capture and len(moves) > 0:
                    move_dict[piece_hash] = moves
            else:
                move_dict[piece_hash] = moves
        return move_dict
