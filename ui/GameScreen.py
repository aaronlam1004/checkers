import math
from typing import List, Tuple

import pygame
from pygame.surface import Surface

from board.Board import Board, Player, PlayerId

class GameScreen:
    def __init__(self):
        # TODO: default options
        self.options = {}
        
    # TODO: load options

    def draw_board(self, screen: Surface, board: Board, scalars: Tuple[float, float]):
        color_white = (227, 182, 84)
        color_black = (179, 142, 64)
        x = 0
        y = 0
        scalar_x, scalar_y = scalars
        for row in range(board.size):
            for col in range(board.size):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(screen, color_white, (x, y, scalar_x, scalar_y))
                else:
                    pygame.draw.rect(screen, color_black, (x, y, scalar_x, scalar_y))
                x += scalar_x
            x = 0
            y += scalar_y
            
    def draw_pieces(self, screen: Surface, player: Player, size: int, scalars: Tuple[float, float], reverse: bool = False):
        if player.id == PlayerId.ONE:
            color_player_fg = (186, 63, 52)
            color_player_bg = (235, 106, 106)
        else:
            color_player_fg = (43, 42, 40)
            color_player_bg = (61, 60, 56)
        
        scalar_x, scalar_y = scalars
        for piece in player.pieces:
            if not reverse:
                x = piece.col
                y = piece.row
            else:
                x = (size - 1) - piece.col
                y = (size - 1) - piece.row
            x *= scalar_x
            y *= scalar_y
            if piece.is_king:
                # TODO: draw king
                pass
            pad = 5
            pygame.draw.ellipse(screen, color_player_bg, (x, y, scalar_x, scalar_y))
            pygame.draw.ellipse(screen, color_player_fg, (x + pad, y + pad, scalar_x - (pad * 2), scalar_y - (pad * 2)))
        
    
    def draw_game(self, screen: Surface, board: Board, resolution: Tuple[int, int], reverse: bool = False):
        width, height = resolution
        scalars = (width / board.size, height / board.size)
        self.draw_board(screen, board, scalars)
        self.draw_pieces(screen, board.players[PlayerId.ONE], board.size, scalars, reverse)
        self.draw_pieces(screen, board.players[PlayerId.TWO], board.size, scalars, reverse)
