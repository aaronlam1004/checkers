import pygame
import socket
from graphics import *
from events import *

from board.Board import * 
from board.StandardBoard import StandardBoard

class Game(object):
    def __init__(self, board="standard", name="Checkers", n=8, length=600, border=20, reflect=False):
        if board == "standard":
            self.board = StandardBoard()
        self.n = n
        self.reflect = reflect

        self.width = length
        self.height = length 
        self.border = border
        self.canvas = Canvas(length, border, name)
        self.ready = False

        self.button_col = (247, 103, 54)
        self.highlight = (81, 237, 122)

    def make_board(self):
        self.board.initialize(self.n)
        # self.board.import_game("./gamestate2.txt")
        # self.board.turn = 1
        if self.reflect:
            self.board.reflect()

    def home_screen(self):
        button_area = (0, 0, 0, 0)
        button_high = False
        running = True
        while running:
            screen = self.canvas.screen

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if is_in_button_area(button_area):
                        self.play_local()
                        running = False
                elif event.type == pygame.MOUSEMOTION:
                    if is_in_button_area(button_area):
                        button_high = True
                    else:
                        button_high = False

            screen.fill((255, 255, 255))
            width, height = screen.get_rect().size
            fontsize = int(100*height/self.width)
            titlefont = pygame.font.SysFont("Comic Sans MS", fontsize)
            textsurface = titlefont.render("Checkers", False, (0, 0, 0))
            twidth, theight = textsurface.get_rect().size
            x = width / 2 - (twidth / 2)
            y = height / 4 - (theight / 2)
            screen.blit(textsurface, (x, y))

            fontsize = int(fontsize / 2)
            bwidth = 200 * (height / self.width)
            bheight = 100 * (height / self.width)
            x = width / 2 - (bwidth / 2)
            y = height / 2
            buttonfont = pygame.font.SysFont("Comic Sans MS", fontsize)

            if not button_high:
                draw_button(screen, "PLAY", buttonfont, (0, 0, 0), (x, y), (bwidth, bheight), self.button_col)
            else:
                draw_button(screen, "PLAY", buttonfont, (0, 0, 0), (x, y), (bwidth, bheight), self.highlight)

            button_area = (x, x + bwidth, y, y + bheight)

            self.canvas.update()

        pygame.quit()

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
                    opp.sendall(b"goodbye")
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

        pygame.quit()

    def game_over(self, player=None, opp=None):
        self.opp_ready = False
        self.running = True
        button_area = (0, 0, 0, 0)
        button_high = False
        while self.running:
            if self.opp_ready and self.ready:
                self.play_online(player, opp)
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if player != None and opp != None:
                        opp.sendall(b"goodbye")
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if is_in_button_area(button_area):
                        if player != None and opp != None:
                            opp.sendall(b"ready")
                            self.ready = True
                        else:
                            self.play_local()
                            self.running = False
                elif event.type == pygame.MOUSEMOTION:
                    if is_in_button_area(button_area):
                        button_high = True
                    else:
                        button_high = False

            screen = self.canvas.screen
            resol = screen.get_rect().size
            
            draw_board(screen, self.board, resol, self.border, self.n, [[], []], None, show=False)

            width, height = screen.get_rect().size
            fontsize = int(75 * height / self.height)
            titlefont = pygame.font.SysFont("Comic Sans MS", fontsize)
            if self.board.state() == 0:
                textsurface = titlefont.render(f"Player {self.board.state() + 1} wins!!", False, (255, 0, 0))
            else:
                textsurface = titlefont.render(f"Player {self.board.state() + 1} wins!!", False, (0, 0, 0))
            twidth, _ = textsurface.get_rect().size
            x = width / 2 - (twidth / 2)
            screen.blit(textsurface, (x, self.border))

            if self.ready:
                titlefont = pygame.font.SysFont("Comic Sans MS", int(fontsize / 2))
                textsurface = titlefont.render(f"Waiting for other player", False, (255, 255, 255))
                twidth, theight = textsurface.get_rect().size
                x = width / 2 - (twidth / 2)
                y = height / 3 - (theight / 2)
                pygame.draw.ellipse(screen, (100, 100, 100), (x-(twidth/8), y-(theight/2), twidth+(twidth/4), 2*theight))
                screen.blit(textsurface, (x, y))

            fontsize = int(fontsize / 2)
            bwidth = 400 * (height / self.width)
            bheight = 100 * (height / self.width)
            x = width / 2 - (bwidth / 2)
            y = height / 2
            buttonfont = pygame.font.SysFont("Comic Sans MS", fontsize)

            if not button_high:
                draw_button(screen, "PLAY AGAIN", buttonfont, (0, 0, 0), (x, y), (bwidth, bheight), self.button_col)
            else:
                draw_button(screen, "PLAY AGAIN", buttonfont, (0, 0, 0), (x, y), (bwidth, bheight), self.highlight)

            button_area = (x, x + bwidth, y, y + bheight)

            self.canvas.update()

    pygame.quit()


class Canvas(object):
    def __init__(self, length, border, name):
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

if __name__ == "__main__":
    g = Game()
    g.home_screen()
