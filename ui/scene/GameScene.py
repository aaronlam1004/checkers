import pygame
from pygame.surface import Surface

from board.Board import Board, BoardState, PlayerId
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
        return Signals.NONE, None

    def draw(self):
        self.screen.fill((40, 40, 40))
        self.board_ui.draw()

    def draw_status(self):
        status_width = 150
        status_height = 50
        x = self.width - status_width
        top_y = 0
        bottom_y = self.height - status_height
        if self.board.turn == PlayerId.ONE:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, bottom_y, status_width, status_height))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), (x, top_y, status_width, status_height))
        

    def update(self):
        self.draw()
        self.draw_status()
        self.board.update()
