import pygame
from pygame.surface import Surface

from Resources import *
from board.Board import Board, BoardState, PlayerId

from ui.scene.Scene import Scene, SceneId
from ui.Button import Button, ButtonColors
from ui.IconButton import IconButton
from ui.BoardUI import BoardUI
from ui.EventHandler import EventHandler, Signals

class GameScene(Scene):
    def __init__(self, screen: Surface, board: Board):
        self.id = SceneId.GAME
        self.options = {}
        self.screen = screen
        self.width, self.height = screen.get_rect().size
        self.board = board
        self.board_ui = BoardUI(self.screen, board, (600, 600), (100, 50))
        self.create_buttons()

        # Signals
        self.home_clicked = False

    def create_buttons(self):
        home_button_colors = ButtonColors(
            (255, 0, 0),
            (0, 0, 0),
            border=(255, 255, 255)
        )
        home_button = IconButton(self.screen, (15, 50), (70, 70), Images.HOME.value, home_button_colors, self.handle_home_button)

        surrender_button = Button(self.screen, (15, 125), (70, 70), "", home_button_colors, self.handle_home_button)
        self.buttons = [
            home_button,
            surrender_button
        ]

    def handle_home_button(self):
        self.home_clicked = True

    # @override
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in self.buttons:
                button.click(mouse_x, mouse_y)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.handle_home_button()
                
        if self.home_clicked:
            self.home_clicked = False
            return Signals.HOME, None

        if self.board.state() == BoardState.NEUTRAL:
            return self.board_ui.handle_event(event)
        return Signals.NONE, None

    def draw(self):
        self.screen.fill((20, 20, 20))
        self.board_ui.draw()

    def draw_status(self):
        status_width = 150
        status_height = 50
        x = (self.width - status_width)
        top_y = 0
        bottom_y = self.height - status_height
        
        border = 8
        if self.board.turn == PlayerId.ONE:
            pygame.draw.rect(self.screen, (255, 255, 255), (x, bottom_y, status_width, status_height))
            pygame.draw.rect(self.screen, (186, 63, 52), (x + (border / 2), bottom_y + (border / 2), status_width - border, status_height - border))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), (x, top_y, status_width, status_height))
            pygame.draw.rect(self.screen, (43, 42, 40), (x + (border / 2), top_y + (border / 2), status_width - border, status_height - border))
        self.draw_time_text(status_width, status_height, top_y, bottom_y)

    def draw_time_text(self, status_width: float, status_height: float, top_y: float, bottom_y: float):
        for player in self.board.players:
            draw_text = f"{player.id + 1}"
            if self.board.blitz_mode:
                time_remaining_s = self.board.player_loss_timeout_s - player.time_elapsed_s
                if time_remaining_s < 0:
                    time_remaining_s = 0
                draw_text = "%.2f" % round(time_remaining_s, 2)
            font_size = int(status_height / 2.5)
            text_font = pygame.font.Font(Fonts.STAR_BORN.value, font_size)
            text_color = (128, 128, 128)
            if self.board.turn == player.id:
                text_color = (255, 255, 255)    
            text_render = text_font.render(draw_text, False, text_color)
            text_width, text_height = text_render.get_rect().size
            text_x = (self.width - (status_width / 2) - (text_width / 2.5))
            if player.id == PlayerId.ONE:
                text_y = bottom_y + (text_height / 2)
                self.screen.blit(text_render, (text_x, text_y))
            else:
                text_y = top_y + (text_height / 2)
                self.screen.blit(text_render, (text_x, text_y))
                
        
    def update(self):
        self.draw()
        for button in self.buttons:
            button.draw()
        self.draw_status()
        self.board.update()
