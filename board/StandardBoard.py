from typing import List, Tuple
from board.Board import *

class StandardBoard(Board):
    def __init__(self):
        super().__init__(size=8)

    # @override
    def get_piece_capture_moves(self, piece: Piece):
        row = piece.row
        col = piece.col
        moves = []
        can_capture = 0
        if piece.is_king or piece.player == PlayerId.ONE:
            if self.check_in_bounds(row - 1, col - 1) and self.board[row - 1][col - 1] != -1:
                neighbor_piece = self.board[row - 1][col - 1]
                if neighbor_piece.player != piece.player:
                    if self.check_in_bounds(row - 2, col - 2) and self.board[row - 2][col - 2] == -1:
                        moves.append(((row - 2, col - 2), neighbor_piece))
                        can_capture = True
            if self.check_in_bounds(row - 1, col + 1) and self.board[row - 1][col + 1] != -1:
                neighbor_piece = self.board[row - 1][col + 1]
                if neighbor_piece.player != piece.player:
                    if self.check_in_bounds(row - 2, col + 2) and self.board[row - 2][col + 2] == -1:
                        moves.append(((row - 2, col + 2), neighbor_piece))
                        can_capture = True
        if piece.is_king or piece.player == PlayerId.TWO:
            if self.check_in_bounds(row + 1, col - 1) and self.board[row + 1][col - 1] != -1:
                neighbor_piece = self.board[row + 1][col - 1]
                if neighbor_piece.player != piece.player:
                    if self.check_in_bounds(row + 2, col - 2) and self.board[row + 2][col - 2] == -1:
                        moves.append(((row + 2, col - 2), neighbor_piece))
                        can_capture = True
            if self.check_in_bounds(row + 1, col + 1) and self.board[row + 1][col + 1] != -1:
                neighbor_piece = self.board[row + 1][col + 1]
                if neighbor_piece.player != piece.player:                
                    if self.check_in_bounds(row + 2, col + 2) and self.board[row + 2][col + 2] == -1:
                        moves.append(((row + 2, col + 2), neighbor_piece))
                        can_capture = True
        return moves, can_capture

    # @override
    def get_piece_moves(self, piece: Piece):
        moves = []
        can_capture = False
        row = piece.row
        col = piece.col
        if row != -1 or col != -1:
            moves, can_capture = self.get_piece_capture_moves(piece)
            if len(moves) == 0:
                if piece.is_king or piece.player == PlayerId.ONE:
                    if self.check_in_bounds(row - 1, col - 1) and self.board[row - 1][col - 1] == -1:
                        moves.append(((row - 1, col - 1), None))
                    if self.check_in_bounds(row - 1, col + 1) and self.board[row - 1][col + 1] == -1:
                        moves.append(((row - 1, col + 1), None))
                if piece.is_king or piece.player == PlayerId.TWO:
                    if self.check_in_bounds(row + 1, col - 1) and self.board[row + 1][col - 1] == -1:
                        moves.append(((row + 1, col - 1), None))
                    if self.check_in_bounds(row + 1, col + 1) and self.board[row + 1][col + 1] == -1:
                        moves.append(((row + 1, col + 1), None))
        return moves, can_capture

    # @override
    def get_all_moves(self):
        has_capture_move = False
        move_dict = {}
        print("TURN", self.turn)
        player = self.players[self.turn]
        for piece in player.pieces:
            moves, can_capture = self.get_piece_moves(piece)
            piece_hash = (piece.row, piece.col)

            # TODO: add not force capture
            if can_capture:
                if not has_capture_move:
                    move_dict = {}
                    has_capture_move = True
                move_dict[piece_hash] = { move[0]: move[1] for move in moves }
            elif not has_capture_move and len(moves) > 0:
                move_dict[piece_hash] = { move[0]: move[1] for move in moves }
        return move_dict
                

# class StandardBoard(Board):
#     def __init__(self):
#         super().__init__()
# 
#     def capture_moves(self, row, col, moves, captures, isking):
#         """
#         Checks to see if a piece can be captured and, if it can, keeps track of which moves capture which pieces.
#         """
#         if self.turn == self.focus or self.turn == self.focus ^ 1 and isking:
#             if self.in_bounds(row - 1, col - 1):
#                 if type(self.board[row - 1][col - 1]) is Piece and self.board[row - 1][col - 1].player == self.turn ^ 1:
#                     if self.in_bounds(row - 2, col - 2) and self.board[row - 2][col - 2] == '-':
#                         captures.append(self.board[row - 1][col - 1])
#                         moves.append((row - 2, col - 2))
#             if self.in_bounds(row - 1, col + 1):
#                 if type(self.board[row - 1][col + 1]) is Piece and self.board[row - 1][col + 1].player == self.turn ^ 1:
#                     if self.in_bounds(row - 2, col + 2) and self.board[row - 2][col + 2] == '-':
#                         captures.append(self.board[row - 1][col + 1])
#                         moves.append((row - 2, col + 2))
# 
#         if self.turn == self.focus ^ 1 or self.turn == self.focus and isking:
#             if self.in_bounds(row + 1, col - 1):
#                 if type(self.board[row + 1][col - 1]) is Piece and self.board[row + 1][col - 1].player == self.turn ^ 1:
#                     if self.in_bounds(row + 2, col - 2) and self.board[row + 2][col - 2] == '-':
#                         captures.append(self.board[row + 1][col - 1])
#                         moves.append((row + 2, col - 2))
#             if self.in_bounds(row + 1, col + 1):
#                 if type(self.board[row + 1][col + 1]) is Piece and self.board[row + 1][col + 1].player == self.turn ^ 1:
#                     if self.in_bounds(row + 2, col + 2) and self.board[row + 2][col + 2] == '-':
#                         captures.append(self.board[row + 1][col + 1])
#                         moves.append((row + 2, col + 2))
# 
#     def get_piece_moves(self, piece):
#         """
#         Get all the possible moves for the current piece.
#         """
#         moves = []
#         captures = []
#         row = piece.row
#         col = piece.col
#         self.capture_moves(row, col, moves, captures, piece.isking)
#         if len(moves) == 0:
#             if piece.player == self.focus or piece.player == self.focus ^ 1 and piece.isking:
#                 if self.in_bounds(row - 1, col - 1) and self.board[row - 1][col - 1] == '-':
#                     moves.append((row - 1, col - 1))
#                 if self.in_bounds(row - 1, col + 1) and self.board[row - 1][col + 1] == '-':
#                     moves.append((row - 1, col + 1))
#             if piece.player == self.focus ^ 1 or piece.player == self.focus and piece.isking:
#                 if self.in_bounds(row + 1, col - 1) and self.board[row + 1][col - 1] == '-':
#                     moves.append((row + 1, col - 1))
#                 if self.in_bounds(row + 1, col + 1) and self.board[row + 1][col + 1] == '-':
#                     moves.append((row + 1, col + 1))
#         return moves, captures
#         
#     def get_all_possible_moves(self):
#         """
#         Gets all the possible moves available that a player can make according to the
#         "standard" rules of checkers.
#         """
#         p = []
#         m = []
#         can_capture = False
#         turn = str(self.turn)
#         index = 0
#         for piece in self.pieces[turn][:self.end[turn]]:
#             moves, captures = self.get_piece_moves(piece)
#             if not can_capture and len(captures) > 0:
#                 can_capture = True
#                 index = len(p)
#             if can_capture and len(captures) > 0:
#                 p.append(piece)
#                 m.append(moves)
#             elif not can_capture and len(moves) > 0:
#                 p.append(piece)
#                 m.append([moves, captures])
#         return p[index:], m[index:]    
