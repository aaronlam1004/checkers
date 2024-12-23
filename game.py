import pygame
import socket

from checkers import Canvas, Checkers
from home import Home
from graphics import *
from events import *

from board.Board import * 
from board.StandardBoard import StandardBoard

if __name__ == "__main__":
    canvas = Canvas()
    checkers = Checkers(canvas)
    home = Home(canvas, checkers)
    home.show()
