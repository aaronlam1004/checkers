import pygame
import socket
from graphics import *
from events import *

from board.Board import * 
from board.StandardBoard import StandardBoard

class Game(object):
    def __init__(self, board="standard", name="Checkers", n=8, length=500, border=20, reflect=False):
        if board == "standard":
            self.board = StandardBoard()

        self.n = n
        self.board.initialize(n)

        if reflect:
            self.board.reflect()

        # self.mode = "online"

        self.width = length
        self.height = length 
        self.border = border
        self.canvas = Canvas(length, border, name)

    def home_screen(self):
        return None

    def play_online(self, player, opp):
        running = True
        captor = None
        sel_piece = None
        sel_moves = [[], []]
        valid = []
        while running:
            if self.board.state() != -1:
                break

            self.canvas.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    piece, moves, coords = get_selected_piece(self.canvas.screen, self.board, self.border, self.n, valid)
                    if piece != None and len(moves[0]) > 0:
                        sel_piece = piece
                        sel_moves = moves
                    else:
                        if sel_piece != None:
                            prev_row = sel_piece.row
                            prev_col = sel_piece.col

                        next_piece, next_moves, capture, flag = move_piece(self.board, sel_piece, sel_moves, coords)

                        if flag == 1:
                            mess = f"{self.board.turn}\n{prev_row} {prev_col}\n{sel_piece.row} {sel_piece.col}"
                            if capture != None:
                                mess += f"\n{capture.row} {capture.col}"
                            opp.sendall(bytes(mess, "utf-8"))

                        sel_piece = next_piece
                        sel_moves = next_moves

                        if sel_piece != None:
                            valid = [sel_piece]
                            captor = sel_piece
                        else:
                            captor = None

            screen = self.canvas.screen
            resol = screen.get_rect().size
            
            if self.board.turn == player:
                valid = draw_board(screen, self.board, resol, self.border, self.n, sel_moves, captor)
            else:
                valid = draw_board(screen, self.board, resol, self.border, self.n, sel_moves, captor, show=False)

            self.canvas.update()


    def play_local(self):
        running = True
        captor = None
        sel_piece = None
        sel_moves = [[], []]
        valid = []
        while running:
            self.canvas.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    piece, moves, coords = get_selected_piece(self.canvas.screen, self.board, self.border, self.n, valid)
                    if piece != None and len(moves[0]) > 0:
                        sel_piece = piece
                        sel_moves = moves
                    else:
                        sel_piece, sel_moves, _, _ = move_piece(self.board, sel_piece, sel_moves, coords)
                        if sel_piece != None:
                            valid = [sel_piece]
                            captor = sel_piece
                        else:
                            captor = None

            screen = self.canvas.screen
            resol = screen.get_rect().size
            valid = draw_board(screen, self.board, resol, self.border, self.n, sel_moves, captor)

            self.canvas.update()


class Canvas(object):
    def __init__(self, length, border, name):
        self.width = length 
        self.height = length
        self.border = border
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()
