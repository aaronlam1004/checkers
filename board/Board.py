class Piece(object):
    def __init__(self, row, col, player, index):
        self.row = row
        self.col = col
        self.isking = False
        self.player = player
        if player == 0:
            self.desc = 'r'
        else:
            self.desc = 'b'
        self.index = index
    
    def __str__(self):
        return str(self.desc)

    def stringify(self):
        return f"Piece [{self.desc}] (({self.row},{self.col}), {self.player}, {self.index})"
    
    def playstring(self):
        return f"Piece [{self.desc}] ({self.row},{self.col})"

    def promote(self):
        self.desc = self.desc.upper() 
        self.isking = True

    def update_coord(self, coord):
        self.row = coord[0]
        self.col = coord[1]

class Board(object):
    def __init__(self):
        self.turn = 0
        self.pieces = {'0': [], '1': []}
        self.end = {'0': 0, '1': 0}
        self.focus = 0

    def __str__(self):
        board = '  ' +  " ".join(str(i) for i in range(self.n)) + '\n'
        for row in range(len(self.board)):
            board += str(row) + ' '
            for col in range(len(self.board[row])):
                board += str(self.board[row][col]) + ' '
            board += '\n'
        return board

    def initialize(self, n):
        """
        Initializes a board of size (n x n) and places pieces like 
        for an actual checkers game.
        """
        self.__init__()
        self.n = n
        self.board = [['-' for _ in range(n)] for i in range(n)]

        n_rows = 3
        for i in range(n_rows):
            for j in range((i + 1) % 2, self.n, 2):
                piece = Piece(i, j, 1, self.end['1'])
                self.end['1'] += 1
                self.board[i][j] = piece
                self.pieces['1'].append(piece)
            for j in range((self.n - i) % 2, self.n, 2):
                bottom = (self.n - 1) - i
                piece = Piece(bottom, j, 0, self.end['0'])
                self.end['0'] += 1
                self.board[bottom][j] = piece 
                self.pieces['0'].append(piece)

    def import_game(self, gamefile):
        """
        Read a text file of a checkers game and load it in. 
        """
        self.__init__()
        self.board = []
        r = 0
        n = 0
        with open(gamefile, 'r') as f:
            for line in f:
                row = []
                c = 0
                for ch in line.rstrip('\n').split(' '):
                    if ch != '-':
                        if ch.upper() == 'R':
                            p = Piece(r, c, 0, self.end['0'])
                            if ch == 'R':
                                p.promote()
                            self.pieces['0'].append(p)
                            self.end['0'] += 1
                            row.append(p)
                        else:
                            p = Piece(r, c, 1, self.end['1'])
                            if ch == 'B':
                                p.promote()
                            self.pieces['1'].append(p)
                            self.end['1'] += 1
                            row.append(p)
                    else:
                        row.append('-')
                    c += 1
                n = c
                self.board.append(row)
                r += 1
        assert r == c
        self.n = n

    def change_turn(self):
        """
        Changes whose turn it is (player 1 or 2)
        """
        self.turn = self.turn ^ 1

    def state(self):
        """
        Checks the state of the board.
             0: means that player 1 wins since all of player 2's pieces have been captured
             1: means that player 2 wins since all of player 1's pieces have been captured
            -1: means neither player has won since pieces from both players remain
        """
        if self.end['1'] == 0: # Player 1 wins
            return 0
        elif self.end['0'] == 0: # Player 2 wins
            return 1
        else: # Game still keeps going 
            return -1

    def get_piece(self, coord):
        """
        Uses the (x, y) coordinates from coord to specify a certain piece on the board. 
        If None, that means the space at coord is empty or is not the current player's piece.
        """
        try:
            piece = self.board[coord[0]][coord[1]]
            if piece.player == self.turn:
                return piece
            return None
        except:
            return None

    def make_move(self, piece, coord, capture):
        """
        Moves a piece on the board from it's current location to coord (x, y).
        Captures all the pieces from captures.
        Promotes the piece if the piece is able to be promoted.
        """
        promoted = False
        self.board[piece.row][piece.col] = '-'
        piece.update_coord(coord)
        if (piece.row == 0 and self.turn == 0) or (piece.row == self.n - 1 and self.turn == 1) and not piece.isking:
            piece.promote()
            promoted = True
        self.board[piece.row][piece.col] = piece
        opp = str(self.turn ^ 1)
        if capture != None:
            index = capture.index
            for val in self.pieces[opp][self.end[opp]:]:
                if val.index < capture.index:
                    index -= 1
            self.board[capture.row][capture.col] = '-'
            removed = self.pieces[opp].pop(index)
            self.pieces[opp].append(removed)
            self.end[opp] -= 1
            if not promoted:
                return self.get_piece_moves(piece)
            return [], []
        else:
            return [], []

    def in_bounds(self, row, col):
        """
        Checks to see if row and col are within the bounds of the board.
        """
        return row >= 0 and row < self.n and col >= 0 and col < self.n

    def reflect(self):
        """
        Reflects the board (as if it is in the view of the opponent's turn)
        """
        for piece in self.pieces['0'][:self.end['0']]:
            if str(self.board[piece.row][piece.col]) == piece.desc:
                self.board[piece.row][piece.col] = '-'
            row = (self.n - 1) - piece.row
            col = (self.n - 1) - piece.col 
            piece.update_coord((row, col))
            self.board[piece.row][piece.col] = piece
        for piece in self.pieces['1'][:self.end['1']]:
            if str(self.board[piece.row][piece.col]) == piece.desc:
                self.board[piece.row][piece.col] = '-'
            row = (self.n - 1) - piece.row
            col = (self.n - 1) - piece.col 
            piece.update_coord((row, col))
            self.board[piece.row][piece.col] = piece
        self.focus = 1

    def reflect_move(self, coords):
        row = coords[0]
        col = coords[1]
        newr = (self.n - 1) - row
        newc = (self.n - 1) - col
        return (newr, newc) 
