from typing import List, Tuple, Optional
from enum import IntEnum
from dataclasses import dataclass

@dataclass
class Piece:
    row: int
    col: int
    player: int
    is_king: bool = False
    
@dataclass
class Player:
    id: int
    pieces: List[Piece]
    captured: int = 0

class PlayerId(IntEnum):
    ONE = 0
    TWO = 1

class BoardState(IntEnum):
    INVALID   = -1
    NEUTRAL   =  0
    RED_WIN   =  1
    BLACK_WIN =  2

class Board:
    def __init__(self, size: int):
        """
        """
        self.size = size
        self.moves_dict = {}

    def setup(self):
        """
        """
        self.board = [[-1 for _ in range(self.size)] for _ in range(self.size)]
        self.load()

    def load(self):
        """
        Initializes standard game
        """
        # RED always goes first
        self.turn = PlayerId.ONE
        
        # Setup players
        self.players = [
            Player(PlayerId.ONE, []),
            Player(PlayerId.TWO, [])
        ]
        
        # Only place pieces on the first 3 rows
        for row in range(3):
            for col in range((row + 1) % 2, self.size, 2):
                piece = Piece(row, col, PlayerId.TWO)
                self.players[PlayerId.TWO].pieces.append(piece)
                self.board[row][col] = piece
            bottom = (self.size - 1) - row
            for col in range((bottom + 1) % 2, self.size, 2):
                piece = Piece(bottom, col, PlayerId.ONE)
                self.players[PlayerId.ONE].pieces.append(piece)
                self.board[bottom][col] = piece

        self.moves_dict = self.get_all_moves()

    def state(self):
        """
        """
        if len(self.players) != 2:
            return BoardState.INVALID
        if self.players[PlayerId.ONE].captured == len(self.players[PlayerId.TWO].pieces):
            return BoardState.RED_WIN
        if self.players[PlayerId.TWO].captured == len(self.players[PlayerId.ONE].pieces):
            return BoardState.BLACK_WIN
        return BoardState.NEUTRAL

    def check_in_bounds(self, row: int, col: int):
        """
        """
        return row >= 0 and row < self.size and col >= 0 and col < self.size

    def check_on_edge(self, row: int, col: int):
        """
        """
        if self.turn == PlayerId.ONE:
            return row == 0
        else:
            return row == self.size - 1

    def find_piece(self, row: int, col: int):
        """
        """
        if self.check_in_bounds(row, col):
            return self.board[row][col]
        return -1

    def get_piece_capture_moves(self, piece: Piece):
        """
        """
        return [], False
    
    def get_piece_moves(self, piece: Piece):
        """
        """
        return [], False

    def get_all_moves(self):
        """
        """
        return {}

    def move(self, piece: Piece, coord: Tuple[int, int], capture: Optional[Piece] = None):
        """
        """
        change_turn = True
        row, col = coord
        if self.check_in_bounds(row, col):
            self.board[piece.row][piece.col] = -1
            self.board[row][col] = piece
            piece.row = row
            piece.col = col
            if self.check_on_edge(row, col):
                piece.is_king = True
            if capture is not None:
                self.players[self.turn].captured += 1
                self.board[capture.row][capture.col] = -1
                capture.row = -1
                capture.col = -1                
                moves, can_capture = self.get_piece_capture_moves(piece)
                if can_capture:
                   change_turn = False
                   self.moves_dict = {
                       (piece.row, piece.col): moves
                   }
            if change_turn:
                self.turn = PlayerId.TWO if self.turn == PlayerId.ONE else PlayerId.ONE
                self.moves_dict = self.get_all_moves()
