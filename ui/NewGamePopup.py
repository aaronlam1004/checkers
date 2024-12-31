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
from ui.CheckButton import CheckButton
import ui.GraphicUtils as GraphicUtils

class NewGamePopup(Popup):
    def __init__(self, screen: Surface, parent: Scene):
        self.parent = parent
        self.player_win_id = -1
        super().__init__(screen)
        self.height = (self.screen_height * 0.75) - (self.margin * 2)
        self.y = (self.screen_height - self.height) * 0.75
        self.create_buttons()

    def set_player_win(self, player_win_id: int) -> None:
        self.player_win_id = player_win_id

    def create_buttons(self) -> None:
        button_margin = 25
        button_width = self.width - (button_margin * 2)
        button_height = 50
        x = self.margin + (button_margin)

        check_y = self.y + (self.height / 4) - button_height
        blitz_check_button = CheckButton(self.screen, (x, check_y), (button_width, button_height), "BLITZ MODE", UI_BUTTON_COLORS, selected=True)
        check_y += button_height + 10
        force_capture_check_button = CheckButton(self.screen, (x, check_y), (button_width, button_height), "FORCE CAPTURE", UI_BUTTON_COLORS)      
        check_y += button_height + 10
        all_kings_check_button = CheckButton(self.screen, (x, check_y), (button_width, button_height), "ALL KINGS", UI_BUTTON_COLORS)
        
        y = self.y + ((self.height * 2) / 3)
        start_button = Button(self.screen, (x, y), (button_width , button_height), "START", UI_BUTTON_COLORS, self.handle_start_button)
        y += button_height + 10
        close_button = Button(self.screen, (x, y), (button_width, button_height), "CLOSE", UI_BUTTON_COLORS, self.handle_close_button)
        self.check_buttons = {
            "blitz": blitz_check_button,
            "force_capture": force_capture_check_button,
            "all_kings": all_kings_check_button
        }
        self.buttons = [
            blitz_check_button,
            force_capture_check_button,
            all_kings_check_button,
            start_button,
            close_button
        ]

    def handle_start_button(self) -> None:
        self.hide()
        self.parent.play_clicked = True

    def handle_close_button(self) -> None:
        self.hide()

    # @override
    def draw_popup(self) -> None:
        super().draw_popup()
        self.draw_title()

    def draw_title(self) -> None:
        font_size = int((self.width - self.border_size) / 10)
        text = f"New Game"
        title_font = pygame.font.Font(Fonts.STAR_BORN.value, font_size)
        text_render = title_font.render(text, False, Colors.BLACK.value)
        text_width, text_height = text_render.get_rect().size
        
        x = self.margin + ((self.width - text_width) / 2)
        y = self.y - text_height

        border_text_render = title_font.render(text, False, Colors.WHITE.value)
        GraphicUtils.draw_text_border(self.screen, border_text_render, x, y, 10)
        self.screen.blit(text_render, (x, y))
