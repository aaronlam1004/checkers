import pygame
from pygame.surface import Surface

from board.Board import Board, BoardState
from ui.scene.Scene import Scene, SceneId
from ui.BoardUI import BoardUI
from ui.EventHandler import EventHandler, Signals

class GameScene(Scene):
    def __init__(self, screen: Surface, board: Board):
        self.id = SceneId.GAME
        # TODO: default options
        self.options = {}
        self.screen = screen
        self.width, self.height = screen.get_rect().size
        self.board = board
        self.board_ui = BoardUI(self.screen, board, (600, 600), (100, 50))

    # TODO: load options
    # @override
    def handle_event(self, event):
        if self.board.state() == BoardState.NEUTRAL:
            return self.board_ui.handle_event(event)
        return Signals.NONE

    def update(self):
        self.screen.fill((40, 40, 40))
        self.board_ui.draw()
        # self.draw_status()
