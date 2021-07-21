from board.Board import * 

class StandardBoard(Board):
    def __init__(self):
        super().__init__()

    def capture_moves(self, row, col, moves, captures, isking):
        """
        Checks to see if a piece can be captured and, if it can, keeps track of which moves capture which pieces.
        """
        if self.turn == self.focus or self.turn == self.focus ^ 1 and isking:
            if self.in_bounds(row - 1, col - 1):
                if type(self.board[row - 1][col - 1]) is Piece and self.board[row - 1][col - 1].player == self.turn ^ 1:
                    if self.in_bounds(row - 2, col - 2) and self.board[row - 2][col - 2] == '-':
                        captures.append(self.board[row - 1][col - 1])
                        moves.append((row - 2, col - 2))
            if self.in_bounds(row - 1, col + 1):
                if type(self.board[row - 1][col + 1]) is Piece and self.board[row - 1][col + 1].player == self.turn ^ 1:
                    if self.in_bounds(row - 2, col + 2) and self.board[row - 2][col + 2] == '-':
                        captures.append(self.board[row - 1][col + 1])
                        moves.append((row - 2, col + 2))

        if self.turn == self.focus ^ 1 or self.turn == self.focus and isking:
            if self.in_bounds(row + 1, col - 1):
                if type(self.board[row + 1][col - 1]) is Piece and self.board[row + 1][col - 1].player == self.turn ^ 1:
                    if self.in_bounds(row + 2, col - 2) and self.board[row + 2][col - 2] == '-':
                        captures.append(self.board[row + 1][col - 1])
                        moves.append((row + 2, col - 2))
            if self.in_bounds(row + 1, col + 1):
                if type(self.board[row + 1][col + 1]) is Piece and self.board[row + 1][col + 1].player == self.turn ^ 1:
                    if self.in_bounds(row + 2, col + 2) and self.board[row + 2][col + 2] == '-':
                        captures.append(self.board[row + 1][col + 1])
                        moves.append((row + 2, col + 2))

    def get_piece_moves(self, piece):
        """
        Get all the possible moves for the current piece.
        """
        moves = []
        captures = []
        row = piece.row
        col = piece.col
        self.capture_moves(row, col, moves, captures, piece.isking)
        if len(moves) == 0:
            if piece.player == self.focus or piece.player == self.focus ^ 1 and piece.isking:
                if self.in_bounds(row - 1, col - 1) and self.board[row - 1][col - 1] == '-':
                    moves.append((row - 1, col - 1))
                if self.in_bounds(row - 1, col + 1) and self.board[row - 1][col + 1] == '-':
                    moves.append((row - 1, col + 1))
            if piece.player == self.focus ^ 1 or piece.player == self.focus and piece.isking:
                if self.in_bounds(row + 1, col - 1) and self.board[row + 1][col - 1] == '-':
                    moves.append((row + 1, col - 1))
                if self.in_bounds(row + 1, col + 1) and self.board[row + 1][col + 1] == '-':
                    moves.append((row + 1, col + 1))
        return moves, captures
        
    def get_all_possible_moves(self):
        """
        Gets all the possible moves available that a player can make according to the
        "standard" rules of checkers.
        """
        p = []
        m = []
        can_capture = False
        turn = str(self.turn)
        index = 0
        for piece in self.pieces[turn][:self.end[turn]]:
            moves, captures = self.get_piece_moves(piece)
            if not can_capture and len(captures) > 0:
                can_capture = True
                index = len(p)
            if can_capture and len(captures) > 0:
                p.append(piece)
                m.append(moves)
            elif not can_capture and len(moves) > 0:
                p.append(piece)
                m.append([moves, captures])
        return p[index:], m[index:] 
