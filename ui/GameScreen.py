import math
from typing import List, Tuple

import pygame
from pygame.surface import Surface

from board.Board import Board, Player, PlayerId

class GameScreen:
    def __init__(self, screen: Surface, board: Board, resolution: Tuple[int, int]):
        # TODO: default options
        self.options = {}
        self.screen = screen
        self.board = board
        self.resolution = resolution
        
        self.available_pieces = []
        self.selected_piece = None
        self.selected_moves = {}
        
    # TODO: load options

    def update(self, reverse: bool = False):
        self.handle_events()
        self.draw_game(reverse)

    def get_mouse_board_position(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        width, height = self.screen.get_rect().size
        row = mouse_y // (width // self.board.size)
        col = mouse_x // (height // self.board.size)
        return (row, col)

    def handle_select_piece_event(self):
        row, col = self.get_mouse_board_position()
        moves_dict = self.board.get_all_moves()
        print(moves_dict)
        if (row, col) in moves_dict:
            self.selected_piece = self.board.find_piece(row, col)
            self.selected_moves = moves_dict[(row, col)]
        else:
            self.selected_piece = None
            self.selected_moves = {}

    def handle_move_piece_event(self):
        if self.selected_piece is not None and len(self.selected_moves) > 0:
            row, col = self.get_mouse_board_position()
            if (row, col) in self.selected_moves:
                captured_piece = self.selected_moves[(row, col)]
                self.board.move(self.selected_piece, (row, col), captured_piece)
                self.selected_piece = None
                self.selected_moves = {}

    def handle_events(self):
        # TODO
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("QUIT")
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                print("MOUSE UP")
                self.handle_move_piece_event()                
                self.handle_select_piece_event()

    def draw_game(self, reverse: bool = False):
        width, height = self.resolution
        scalars = (width / self.board.size, height / self.board.size)
        self.draw_board(scalars)
        self.draw_pieces(self.board.players[PlayerId.ONE],  scalars, reverse)
        self.draw_pieces(self.board.players[PlayerId.TWO],  scalars, reverse)

    def draw_board(self, scalars: Tuple[float, float]):
        color_white = (227, 182, 84)
        color_black = (179, 142, 64)
        color_move = (255, 0, 0)
        x = 0
        y = 0
        scalar_x, scalar_y = scalars
        for row in range(self.board.size):
            for col in range(self.board.size):
                square_color = color_black
                if (row, col) in self.selected_moves:
                    square_color = color_move
                elif (row + col) % 2 == 0:
                    square_color = color_white

                pygame.draw.rect(self.screen, square_color, (x, y, scalar_x, scalar_y))
                x += scalar_x
            x = 0
            y += scalar_y
            
    def draw_pieces(self, player: Player, scalars: Tuple[float, float], reverse: bool = False):
        if player.id == PlayerId.ONE:
            color_player_bg = (235, 106, 106)
            color_player_fg = (186, 63, 52)
        else:
            color_player_bg = (61, 60, 56)
            color_player_fg = (43, 42, 40)
        color_player_highlight = (255, 0, 0)
            
        scalar_x, scalar_y = scalars
        for piece in player.pieces:
            if not reverse:
                x = piece.col
                y = piece.row
            else:
                x = (self.board.size - 1) - piece.col
                y = (self.board.size - 1) - piece.row
            if piece.is_king:
                # TODO: draw king
                pass

            if piece == self.selected_piece:
                self.draw_piece(self.screen, x * scalar_x, y * scalar_y, scalar_x, scalar_y, 5, color_player_highlight)
            self.draw_piece(self.screen, x * scalar_x, y * scalar_y, scalar_x, scalar_y, 10, color_player_bg)
            self.draw_piece(self.screen, x * scalar_x, y * scalar_y, scalar_x, scalar_y, 20, color_player_fg)

    def draw_piece(self, screen: Surface, x: float, y: float, width: float, height: float, margin: float, color: Tuple[int, int, int]):
        x += (margin / 2)
        y += (margin / 2)
        pygame.draw.ellipse(self.screen, color, (x, y, width - margin, height - margin))
