from typing import Tuple

import pygame
from pygame.surface import Surface

from Settings import ColorSettings
from Resources import Fonts
from board.Board import PlayerId
from scene.Scene import Scene
from ui.Colors import Colors
from ui.Constants import UI_BUTTON_COLORS
from ui.Popup import Popup
from ui.Button import Button
import ui.GraphicUtils as GraphicUtils

class GameOverPopup(Popup):
    def __init__(self, screen: Surface, parent: Scene):
        self.parent = parent
        self.player_win_id = -1
        super().__init__(screen)
        self.height = (self.screen_height / 2) - (self.margin * 2)
        self.y = (self.screen_height - self.height) / 2
        self.create_buttons()

    def set_player_win(self, player_win_id: int) -> None:
        self.player_win_id = player_win_id

    def create_buttons(self) -> None:
        button_margin = 25
        button_width = self.width - (button_margin * 2)
        button_height = 50
        x = self.margin + (button_margin)
        y = self.y + (self.height / 2) - button_height
        play_again_button = Button(self.screen, (x, y), (button_width , button_height), "PLAY AGAIN", UI_BUTTON_COLORS, self.handle_play_again_button)
        y += button_height + 10
        close_button = Button(self.screen, (x, y), (button_width, button_height), "CLOSE", UI_BUTTON_COLORS, self.handle_close_button)
        self.buttons = [play_again_button, close_button]

    # @override
    def hide(self) -> None:
        self.parent.board.set_idle()
        super().hide()

    def handle_play_again_button(self) -> None:
        self.hide()
        self.parent.board.setup()

    def handle_close_button(self) -> None:
        self.hide()

    # @override
    def draw_popup(self) -> None:
        if self.player_win_id in PlayerId:
            player_color = ColorSettings.player_one
            if self.player_win_id == PlayerId.TWO:
                player_color = ColorSettings.player_two
            piece_width, piece_height = (175, 175)
            piece_x = (self.screen_width - self.margin) - piece_width
            piece_y = self.height - self.margin - (piece_height / 1.75)
            GraphicUtils.draw_piece(self.screen, (piece_x, piece_y), (piece_width, piece_height), player_color, outline_color=Colors.WHITE.value)
        super().draw_popup()
        self.draw_title(self.player_win_id, player_color)

    def draw_title(self, player_id: int, player_color: Tuple[int, int, int]) -> None:
        font_size = int((self.width - self.border_size) / 10)
        text = f"Player {player_id + 1} Wins"
        title_font = pygame.font.Font(Fonts.STAR_BORN.value, font_size)
        text_render = title_font.render(text, False, player_color)
        text_width, text_height = text_render.get_rect().size
        
        x = self.margin + ((self.width - text_width) / 2)
        y = self.y - text_height

        border_text_render = title_font.render(text, False, Colors.WHITE.value)
        GraphicUtils.draw_text_border(self.screen, border_text_render, x, y, 10)
        inside_border_text_render = title_font.render(text, False, ColorSettings.get_bg_color(player_color))
        GraphicUtils.draw_text_border(self.screen, inside_border_text_render, x, y, 4)
        self.screen.blit(text_render, (x, y))
