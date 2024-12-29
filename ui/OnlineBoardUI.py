from typing import Tuple
from socket import socket

import pygame
from pygame.surface import Surface

from board.Board import Board, PlayerId
from ui.BoardUI import BoardUI
from scene.SceneHandler import  SceneSignals

class OnlineBoardUI(BoardUI):
    def __init__(self, screen: Surface, board: Board, dimensions: Tuple[int, int], offset: Tuple[int, int]):
        self.player_id = None
        self.socket = None
        super().__init__(screen, board, dimensions, offset)

    def set_player_id(self, player_id: int):
        if player_id in PlayerId:
            self.player_id = player_id

    def set_socket(self, sock: socket):
        self.socket = sock

    def get_mouse_board_position(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        width, height = self.dimensions
        offset_x, offset_y = self.offset
        row = (mouse_y - offset_y) // (height // self.board.size)
        col = (mouse_x - offset_x) // (width // self.board.size)
        return (row, col)

    def get_select_piece_event(self):
        if self.board.turn == self.player_id:
            return super().get_select_piece_event()
        return None, {}

    def handle_move_piece_event(self):
        current_turn = self.board.turn
        if self.board.turn == self.player_id:
            if self.socket:
                self.socket.sendall(f"{self.player_id} made a move".encode("utf-8"))
            super().handle_move_piece_event()

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
