from typing import Tuple

import pygame
from pygame.surface import Surface

from Settings import ColorSettings
from Resources import Images, Fonts
from board.Board import Board, BoardState, PlayerId
from scene.Scene import Scene, SceneId
from scene.SceneHandler import SceneSignals
from ui.Button import ButtonColors
from ui.IconButton import Button, IconButton
from ui.BoardUI import BoardUI
from ui.Popup import Popup
import ui.GraphicUtils as GraphicUtils

class GameOverPopup(Popup):
    def __init__(self, screen: Surface, parent: Scene):
        self.parent = parent
        self.player_win_id = -1
        super().__init__(screen)
        self.create_buttons()

    def create_buttons(self):
        button_margin = 25
        button_width = self.width - (button_margin * 2)
        button_height = 50
        x = self.margin + (button_margin)
        play_again_button = Button(self.screen, (x, self.height / 2), (button_width , button_height), "PLAY AGAIN", ButtonColors(), self.handle_play_again_button)
        self.buttons.append(play_again_button)

    def set_player_win(self, player_win_id: int):
        self.player_win_id = player_win_id

    # @override
    def hide(self):
        self.parent.board.set_idle()
        super().hide()

    def handle_play_again_button(self):
        self.hide()
        self.parent.board.setup()

    # @override
    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in self.buttons:
                button.click(mouse_x, mouse_y)

    # @override
    def draw(self):
        super().draw()
        if self.visible:
            if self.player_win_id in PlayerId:
                player_color = ColorSettings.player_one
                if self.player_win_id == PlayerId.TWO:
                    player_color = ColorSettings.player_two

                piece_width, piece_height = (150, 150)
                piece_x = (self.screen_width - (self.margin * 2)) - piece_width
                piece_y = self.margin * 2
                GraphicUtils.draw_piece(self.screen, (piece_x, piece_y), (piece_width, piece_height), player_color, outline_color=(255, 255, 255))
                self.draw_title(self.player_win_id, player_color)

    def draw_title(self, player_id: int, player_color: Tuple[int, int, int]):
        font_size = int(self.width / 10)
        text = f"Player {player_id + 1} Wins"
        title_font = pygame.font.Font(Fonts.STAR_BORN.value, font_size)
        text_render = title_font.render(text, False, player_color)
        text_width, text_height = text_render.get_rect().size
        
        x = self.margin + ((self.width - text_width) / 2)
        y = text_height + (self.margin * 1.25)

        border_text_render = title_font.render(text, False, (255, 255, 255))
        GraphicUtils.draw_text_border(self.screen, border_text_render, x, y, 9)
        inside_border_text_render = title_font.render(text, False, ColorSettings.get_bg_color(player_color))
        GraphicUtils.draw_text_border(self.screen, inside_border_text_render, x, y, 4)
        self.screen.blit(text_render, (x, y))
                        

class GameScene(Scene):
    def __init__(self, screen: Surface, board: Board):
        self.id = SceneId.GAME
        self.options = {}
        self.screen = screen
        self.width, self.height = screen.get_rect().size
        self.board = board
        self.board_ui = BoardUI(self.screen, board, (600, 600), (100, 50))
        self.create_buttons()

        # Popup
        self.popup_game_over = GameOverPopup(self.screen, self)

        # Signals
        self.home_clicked = False

    def create_buttons(self):
        button_colors = ButtonColors()
        home_button = IconButton(self.screen, (15, self.height - 125), (70, 70), Images.HOME.value, button_colors, self.handle_home_button)
        surrender_button = IconButton(self.screen, (15, 50), (70, 70), Images.FLAG.value, button_colors, self.handle_surrender_button)
        play_again_button = IconButton(self.screen, (15, 50), (70, 70), Images.REFRESH.value, button_colors, self.handle_play_again_button, visible = False)
        self.buttons = [
            home_button,
            surrender_button,
            play_again_button
        ]

    def handle_home_button(self):
        self.home_clicked = True

    def handle_surrender_button(self):
        # TODO: need to handle when online
        self.board.surrender(self.board.turn)

    def handle_play_again_button(self):
        # TODO: need to handle when online
        self.board.setup()

    # @override
    def handle_event(self, event):
        if self.popup_game_over.visible:
            self.popup_game_over.handle_event(event)
        else:
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in self.buttons:
                    button.click(mouse_x, mouse_y)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.handle_home_button()
            if self.home_clicked:
                self.home_clicked = False
                return SceneSignals.HOME, None
            if self.board.state() == BoardState.NEUTRAL:
                return self.board_ui.handle_event(event)
        return SceneSignals.NONE, None

    def draw(self):
        self.screen.fill((20, 20, 20))
        self.board_ui.draw()
        self.draw_status()

        _, surrender_button, play_again_button = self.buttons
        if self.board.state() == BoardState.IDLE:
            surrender_button.hide()
            play_again_button.show()
        else:
            surrender_button.show()
            play_again_button.hide()
        for button in self.buttons:
            button.draw()
        self.popup_game_over.draw()

    def draw_status(self):
        status_width = 175
        status_height = 45
        x = (self.width - status_width)
        top_y = 0
        bottom_y = self.height - status_height
        
        border = 8
        if self.board.turn == PlayerId.ONE:
            pygame.draw.rect(self.screen, (255, 255, 255), (x, bottom_y, status_width, status_height))
            pygame.draw.rect(self.screen, ColorSettings.player_one, (x + (border / 2), bottom_y + (border / 2), status_width - border, status_height - border))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), (x, top_y, status_width, status_height))
            pygame.draw.rect(self.screen, ColorSettings.player_two, (x + (border / 2), top_y + (border / 2), status_width - border, status_height - border))
        self.draw_player_text(status_width, status_height, top_y, bottom_y)

    def draw_player_text(self, status_width: float, status_height: float, top_y: float, bottom_y: float):
        for player in self.board.players.values():
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
                if player.id == PlayerId.ONE:
                    text_color = ColorSettings.get_contrast_color(ColorSettings.player_one)
                else:
                    text_color = ColorSettings.get_contrast_color(ColorSettings.player_two)  
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
        self.board.update()
        if self.board.state() != BoardState.NEUTRAL and self.board.state() != BoardState.IDLE:
            if self.board.state() == BoardState.RED_WIN:
                self.popup_game_over.set_player_win(PlayerId.ONE)
            else:
                self.popup_game_over.set_player_win(PlayerId.TWO)
            self.popup_game_over.show()
