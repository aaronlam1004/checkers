from typing import Tuple, Callable, Optional

import pygame
from pygame.surface import Surface

from Resources import Fonts
from ui.Button import Button, ButtonColors
import ui.GraphicUtils as GraphicUtils

class CheckButton(Button):
    def __init__(self, screen: Surface, position: Tuple[int, int], dimension: Tuple[int, int],
                 text: str, button_colors: ButtonColors, selected: bool = False,
                 visible: bool = True, border_size: float = 8, border_radius: float = 20):
        self.selected = selected
        self.check_size = 50
        super().__init__(screen, position, dimension, text, button_colors, None, visible, border_size, border_radius)
   
    # @override
    def click(self, mouse_x: int, mouse_y: int):
        if self.visible:
            if self.in_area(mouse_x, mouse_y):
                self.selected = not self.selected

    # @override
    def draw(self):
        if self.visible:
            x = self.x
            y = self.y
            width = self.check_size
            height = self.check_size
            check_color = self.colors.background
            pygame.draw.rect(self.screen, check_color, (x, y, width, height))
            if not self.selected:
                border = 10
                x += (border / 2)
                y += (border / 2)
                width -= border
                height -= border
                pygame.draw.rect(self.screen, self.colors.foreground, (x, y, width, height))
            self.draw_text()

    # @override
    def draw_text(self):
        screen_width, screen_height = self.screen.get_rect().size
        aspect_ratio = screen_width / screen_height

        text_size = min([(self.height / 2), (self.width / 2)])
        font_size = int(text_size * aspect_ratio)
        
        text_font = pygame.font.Font(Fonts.STAR_BORN.value, font_size)

        text_render = text_font.render(self.text, False, self.colors.foreground)
        text_width, text_height = text_render.get_rect().size
        x = self.x + self.check_size + 10
        y = self.y + (self.check_size / 10)
        
        if self.colors.foreground_border:
            border_text_render = text_font.render(self.text, False, self.colors.foreground_border)
            GraphicUtils.draw_text_border(self.screen, border_text_render, x, y, 3)

        self.screen.blit(text_render, (x, y))
