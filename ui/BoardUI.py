import math
from typing import List, Tuple

import pygame
from pygame.surface import Surface

from Settings import ColorSettings
from Resources import Images
from board.Board import Board, Player, PlayerId, Piece
from ui.AudioPlayer import AudioPlayer
from scene.SceneHandler import SceneSignals

class BoardUI:
    def __init__(self, screen: Surface, board: Board, dimensions: Tuple[int, int], offset: Tuple[int, int]):
        self.options = {}
        self.screen = screen
        self.board = board
        self.dimensions = dimensions
        self.offset = offset
        
        self.available_pieces = []
        self.selected_piece = None
        self.selected_moves = {}

        self.drag_piece = False
        
    def update(self):
        self.draw_game()

    def get_mouse_board_position(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        width, height = self.dimensions
        offset_x, offset_y = self.offset
        row = (mouse_y - offset_y) // (height // self.board.size)
        col = (mouse_x - offset_x) // (width // self.board.size)
        return (row, col)

    def get_select_piece_event(self):
        row, col = self.get_mouse_board_position()
        moves_dict = self.board.moves_dict
        if (row, col) in moves_dict:
            return self.board.find_piece(row, col), moves_dict[(row, col)]
            # self.selected_piece = self.board.find_piece(row, col)
            # self.selected_moves = moves_dict[(row, col)]
        else:
            return None, {}
            # self.selected_piece = None
            # self.selected_moves = {}

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            piece, moves = self.get_select_piece_event()
            if piece is not None:
                self.drag_piece = True
            else:
                self.handle_move_piece_event()
                piece, moves = self.get_select_piece_event()
            self.selected_piece = piece
            self.selected_moves = moves
        if event.type == pygame.MOUSEBUTTONUP:
            self.drag_piece = False
            if self.selected_piece:
                self.handle_move_piece_event()
                self.selected_piece, self.selected_moves = self.get_select_piece_event()
        return SceneSignals.NONE, None

    def draw(self):
        width, height = self.dimensions
        scalars = (width / self.board.size, height / self.board.size)
        self.draw_board(scalars)
        self.draw_pieces(self.board.players[PlayerId.ONE], scalars)
        self.draw_pieces(self.board.players[PlayerId.TWO], scalars)

    def draw_board(self, scalars: Tuple[float, float]):
        color_white = ColorSettings.white_tile
        color_black = ColorSettings.black_tile
        color_move = (90, 90, 90)
        color_selected_piece = ColorSettings.selected_tile

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

                radius = 20
                if row == 0 and col == 0:
                    pygame.draw.rect(self.screen, square_color, (x, y, scalar_x, scalar_y), border_top_left_radius=radius)
                elif row == 0 and col == self.board.size - 1:
                    pygame.draw.rect(self.screen, square_color, (x, y, scalar_x, scalar_y), border_top_right_radius=radius)
                elif row == self.board.size - 1 and col == 0:
                    pygame.draw.rect(self.screen, square_color, (x, y, scalar_x, scalar_y), border_bottom_left_radius=radius)
                elif row == self.board.size - 1 and col == self.board.size - 1:
                    pygame.draw.rect(self.screen, square_color, (x, y, scalar_x, scalar_y), border_bottom_right_radius=radius)
                else:
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
            color_player_fg = ColorSettings.player_one
        else:
            color_player_fg = ColorSettings.player_two
        color_player_bg = ColorSettings.get_bg_color(color_player_fg)
        color_player_outline = (0, 0, 0)
        
        for piece in player.pieces:
            self.draw_piece(piece, scalars, color_player_fg, color_player_bg, color_player_outline)

    def draw_piece(self, piece: Piece, scalars: Tuple[float, float], color_fg: Tuple[int, int, int], color_bg: Tuple[int, int, int], color_outline: Tuple[int, int, int]):
        scalar_x, scalar_y = scalars
        if piece.row != - 1 and piece.col != -1:
            is_selected = False
            if self.selected_piece and self.selected_piece.row == piece.row and self.selected_piece.col == piece.col and self.drag_piece:
                x, y = pygame.mouse.get_pos()
                is_selected = True
            else:
                x = piece.col * scalar_x
                y = piece.row * scalar_y
            self.draw_piece_ellipse(x, y, scalar_x, scalar_y, 12, color_outline, is_selected)
            self.draw_piece_ellipse(x, y, scalar_x, scalar_y, 20, color_bg, is_selected)
            self.draw_piece_ellipse(x, y, scalar_x, scalar_y, 28, color_fg, is_selected)
            if piece.is_king:
                self.draw_king(x, y, scalar_x, scalar_y, 28, color_bg, is_selected)

    def draw_piece_ellipse(self, x: float, y: float, width: float, height: float, margin: float, color: Tuple[int, int, int], is_selected: bool):
        if is_selected:
            x -= ((width - margin) / 2)
            y -= ((height - margin) / 2)
        else:
             offset_x, offset_y = self.offset
             x += (margin / 2) + offset_x
             y += (margin / 2) + offset_y
        pygame.draw.ellipse(self.screen, color, (x, y, width - margin, height - margin))

    def draw_king(self, x: float, y: float, width: float, height: float, margin: float, color: Tuple[int, int, int], is_selected: bool):
        offset_x, offset_y = self.offset
        if is_selected:
            x -= ((width - margin) / 2)
            y -= ((height - margin) / 2) 
        else:
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
