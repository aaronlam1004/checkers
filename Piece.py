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
