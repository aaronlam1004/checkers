import pygame
import socket

from checkers import Canvas, Checkers
from home import Home
from graphics import *
from events import *

from board.Board import * 
from board.StandardBoard import StandardBoard

from ui.Window import Window
from ui.GameScreen import GameScreen

if __name__ == "__main__":
    window = Window((600, 600), "Checkers")
    board = StandardBoard()
    board.setup()
    game_screen = GameScreen(window.screen, board, (600, 600), (0, 0))
    running = True
    while running:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        game_screen.update()
        window.update()
    # checkers = Checkers(canvas)
    # home = Home(canvas, checkers)
    # home.show()
