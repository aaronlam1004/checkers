import pygame
import socket

from checkers import Canvas, Checkers
from home import Home
from graphics import *
from events import *

from board.Board import * 
from board.StandardBoard import StandardBoard

from ui.GameScreen import GameScreen

if __name__ == "__main__":
    canvas = Canvas()
    game_screen = GameScreen()
    board = StandardBoard()
    board.setup()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game_screen.draw_game(canvas.screen, board, (600, 600))
        canvas.update()
    # checkers = Checkers(canvas)
    # home = Home(canvas, checkers)
    # home.show()
