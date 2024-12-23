import pygame
import socket
from graphics import *
from events import *

from button import Button
from board.Board import * 
from board.StandardBoard import StandardBoard

NAME = "Checkers"
LENGTH = 600
BORDER = 20

class Canvas(object):
    def __init__(self, length = LENGTH, border = BORDER, name = NAME):
        self.width = length 
        self.height = length
        self.border = border
        # TODO: pygame.RESIZABLE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

class Checkers(object):
    def __init__(self, canvas=None, length=600, border=20, board="standard", name="Checkers", n=8, reflect=False):
        if board == "standard":
            self.board = StandardBoard()
        self.n = n
        self.reflect = reflect

        if canvas is not None:
            self.canvas = canvas            
        else:
            self.canvas = Canvas(length, border, name)
        self.width = self.canvas.width
        self.height = self.canvas.height 
        self.border = self.canvas.border
        self.ready = False

    def make_board(self):
        self.board.initialize(self.n)
        if self.reflect:
            self.board.reflect()

    def play_local(self):
        self.make_board()
        running = True
        captor = None
        sel_piece = None
        sel_moves = [[], []]
        valid = []
        while running:
            if self.board.state() != -1:
                self.game_over()
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

    def play_online(self, player, opp):
        self.ready = False
        self.make_board()
        self.running = True
        captor = None
        sel_piece = None
        sel_moves = [[], []]
        valid = []
        while self.running:
            if self.board.state() != -1:
                self.game_over(player, opp)
                break

            self.canvas.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
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

        opp.sendall(b"goodbye")
        pygame.quit()

    def handle_game_over_events(self, buttons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if player != None and opp != None:
                    opp.sendall(b"goodbye")
                self.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    if button.check_in_area():
                        button.on_click()
            elif event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    button.check_in_area()

    def handle_play_again(self, player, opp):
        if player != None and opp != None:
            opp.sendall(b"ready")
            self.ready = True
        else:
            self.play_local()
            self.running = False

    def game_over(self, player=None, opp=None):
        global options

        p1color = options["p1king"]
        p2color = options["p2king"]

        self.opp_ready = False
        self.running = True

        fontsize = int(75 * self.height / self.height)
        bfontsize = int(fontsize / 2)
        
        bwidth = 400 * (self.height / self.width)
        bheight = 100 * (self.height / self.width)
        bx = self.width / 2 - (bwidth / 2)
        by = self.height / 2
        buttonfont = pygame.font.SysFont("Comic Sans MS", bfontsize)
        buttons = [
            Button(bx, by, bwidth, bheight, "PLAY AGAIN", (247, 103, 54), (81, 237, 122), lambda a=player, b=opp : self.handle_play_again(a, b))
        ]

        while self.running:
            if self.opp_ready and self.ready:
                self.play_online(player, opp)
                break
            self.handle_game_over_events(buttons)
            screen = self.canvas.screen
            resol = screen.get_rect().size
            
            draw_board(screen, self.board, resol, self.border, self.n, [[], []], None, show=False)

            titlefont = pygame.font.SysFont("Comic Sans MS", fontsize)
            if self.board.state() == 0:
                textsurface = titlefont.render(f"Player {self.board.state() + 1} wins!!", False, p1color)
            else:
                textsurface = titlefont.render(f"Player {self.board.state() + 1} wins!!", False, p2color)
            twidth, _ = textsurface.get_rect().size
            x = self.width / 2 - (twidth / 2)
            screen.blit(textsurface, (x, self.border))

            if self.ready:
                titlefont = pygame.font.SysFont("Comic Sans MS", int(fontsize / 2))
                textsurface = titlefont.render(f"Waiting for other player", False, (255, 255, 255))
                twidth, theight = textsurface.get_rect().size
                x = self.width / 2 - (twidth / 2)
                y = self.height / 3 - (theight / 2)
                pygame.draw.ellipse(screen, (100, 100, 100), (x-(twidth/8), y-(theight/2), twidth+(twidth/4), 2*theight))
                screen.blit(textsurface, (x, y))

            for b in buttons:
                draw_button(screen, b.text, buttonfont, (0, 0, 0), (b.x, b.y), (b.width, b.height), b.color)
            self.canvas.update()

    pygame.quit()
