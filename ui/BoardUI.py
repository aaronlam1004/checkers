import math
from typing import List, Tuple

import pygame
from pygame.surface import Surface

from Resources import *
from board.Board import Board, Player, PlayerId
from ui.AudioPlayer import AudioPlayer
from ui.EventHandler import Signals

class BoardUI:
    def __init__(self, screen: Surface, board: Board, dimensions: Tuple[int, int], offset: Tuple[int, int]):
        # TODO: default options
        self.options = {}
        self.screen = screen
        self.board = board
        self.dimensions = dimensions
        self.offset = offset
        
        self.available_pieces = []
        self.selected_piece = None
        self.selected_moves = {}
        
    # TODO: load options

    def update(self):
        self.draw_game()

    def get_mouse_board_position(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        width, height = self.dimensions
        offset_x, offset_y = self.offset
        row = (mouse_y - offset_y) // (height // self.board.size)
        col = (mouse_x - offset_x) // (width // self.board.size)
        return (row, col)

    def handle_select_piece_event(self):
        row, col = self.get_mouse_board_position()
        moves_dict = self.board.moves_dict
        print(moves_dict)
        if (row, col) in moves_dict:
            self.selected_piece = self.board.find_piece(row, col)
            self.selected_moves = moves_dict[(row, col)]
        else:
            self.selected_piece = None
            self.selected_moves = {}

    def handle_move_piece_event(self):
        current_turn = self.board.turn
        if self.selected_piece is not None and len(self.selected_moves) > 0:
            row, col = self.get_mouse_board_position()
            if (row, col) in self.selected_moves:
                captured_piece = self.selected_moves[(row, col)]
                self.board.move(self.selected_piece, (row, col), captured_piece)
                AudioPlayer.play_piece_move()
                if current_turn != self.board.turn:
                    self.selected_piece = None
                    self.selected_moves = {}
                else:
                    self.selected_moves = self.board.moves_dict

    def handle_event(self, event):
        # TODO
        if event.type == pygame.MOUSEBUTTONUP:
            self.handle_move_piece_event()                
            self.handle_select_piece_event()
        return Signals.NONE, None

    def draw(self):
        width, height = self.dimensions
        scalars = (width / self.board.size, height / self.board.size)
        self.draw_board(scalars)
        self.draw_pieces(self.board.players[PlayerId.ONE], scalars)
        self.draw_pieces(self.board.players[PlayerId.TWO], scalars)

    def draw_board(self, scalars: Tuple[float, float]):
        # color_white = (227, 182, 84)
        color_white = (236, 236, 208)
        # color_black = (179, 142, 64)
        color_black = (114, 149, 81)
        color_move = (110, 110, 110)
        color_selected_piece = (255, 235, 59)

        x, y = self.offset
        offset_x, offset_y = self.offset
        scalar_x, scalar_y = scalars
        
        for row in range(self.board.size):
            for col in range(self.board.size):
                square_color = color_black
                if self.selected_piece and row == self.selected_piece.row and col == self.selected_piece.col:
                    square_color = color_selected_piece
                elif (row + col) % 2 == 0:
                    square_color = color_white

                pygame.draw.rect(self.screen, square_color, (x, y, scalar_x, scalar_y))
                if (row, col) in self.selected_moves:
                    pygame.draw.rect(self.screen, square_color, (x, y, scalar_x, scalar_y))
                    move_x = x + (scalar_x / 4)
                    move_y = y + (scalar_y / 4)
                    pygame.draw.ellipse(self.screen, color_move, (move_x, move_y, scalar_x / 2, scalar_y / 2))
                x += scalar_x
            x = offset_x
            y += scalar_y
            
    def draw_pieces(self, player: Player, scalars: Tuple[float, float]):
        if player.id == PlayerId.ONE:
            color_player_bg = (235, 106, 106)
            color_player_fg = (186, 63, 52)
        else:
            color_player_bg = (61, 60, 56)
            color_player_fg = (43, 42, 40)
        color_player_highlight = (0, 0, 0)

        offset_x, offset_y = self.offset
        scalar_x, scalar_y = scalars
        for piece in player.pieces:
            if piece.row != -1 or piece.col != -1:
                x = piece.col
                y = piece.row
                self.draw_piece(x * scalar_x, y * scalar_y, scalar_x, scalar_y, 12, color_player_highlight)
                self.draw_piece(x * scalar_x, y * scalar_y, scalar_x, scalar_y, 20, color_player_bg)
                self.draw_piece(x * scalar_x, y * scalar_y, scalar_x, scalar_y, 30, color_player_fg)
                if piece.is_king:
                    self.draw_king(x * scalar_x, y * scalar_y, scalar_x, scalar_y, 30, color_player_bg)

    def draw_piece(self, x: float, y: float, width: float, height: float, margin: float, color: Tuple[int, int, int]):
        offset_x, offset_y = self.offset
        x += (margin / 2) + offset_x
        y += (margin / 2) + offset_y
        pygame.draw.ellipse(self.screen, color, (x, y, width - margin, height - margin))

    def draw_king(self, x: float, y: float, width: float, height: float, margin: float, color: Tuple[int, int, int]):
        offset_x, offset_y = self.offset
        x += (margin / 2) + offset_x
        y += (margin / 2) + offset_y
        king_img = pygame.image.load(Images.KING.value).convert_alpha()
        king_img = pygame.transform.scale(king_img, (width / 1.75, height / 1.75))
        king_width, king_height = king_img.get_size()
        r, g, b = color
        for row in range(king_width):
            for col in range(king_height):
                _, _, _, alpha = king_img.get_at((row, col))
                king_img.set_at((row, col), pygame.Color(r, g, b, alpha))
        king_rect = (x + 1, y - 1, king_width, king_height)
        self.screen.blit(king_img, king_rect)
