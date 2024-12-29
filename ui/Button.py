from dataclasses import dataclass
from typing import Tuple, Callable, Optional

import pygame
from pygame.surface import Surface

from Resources import Fonts
import ui.GraphicUtils as GraphicUtils

@dataclass
class ButtonColors:
    background: Tuple[int, int, int] = (255, 255, 255)
    foreground: Tuple[int, int, int] = (0, 0, 0)
    highlight: Optional[Tuple[int, int, int]] = None
    border: Optional[Tuple[int, int, int]] = None
    highlight_border: Optional[Tuple[int, int, int]] = None
    foreground_border: Optional[Tuple[int, int, int]] = None

class Button:
    def __init__(self, screen: Surface, position: Tuple[int, int], dimension: Tuple[int, int],
                 text: str, button_colors: ButtonColors, on_click: Optional[Callable[[None], None]],
                 visible: bool = True, border_size: float = 8, border_radius: float = 20):
        self.screen = screen
        self.x, self.y = position
        self.width, self.height = dimension
        self.text = text
        self.on_click = on_click
        self.visible = visible
        self.border_radius = border_radius
        self.border_size = border_size
        self.set_colors(button_colors)

    def set_colors(self, button_colors: ButtonColors):
        self.colors = button_colors
        self.color = self.colors.background
        self.border_color = self.colors.border

    def set_text(self, text: str):
        self.text = text

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def in_area(self, mouse_x: int, mouse_y: int):
        return mouse_x >= self.x and mouse_x <= self.x + self.width and mouse_y >= self.y and mouse_y <= self.y + self.height

    def hover(self, mouse_x: int, mouse_y: int):
        if self.visible:
            if self.in_area(mouse_x, mouse_y):
                if self.colors.highlight:
                    self.color = self.colors.highlight
                if self.colors.highlight_border:
                    self.border_color = self.colors.highlight_border
            else:
                self.color = self.colors.background
                self.border_color = self.colors.border

    def click(self, mouse_x: int, mouse_y: int):
        if self.visible:
            if self.in_area(mouse_x, mouse_y):
                if self.on_click:
                    self.on_click()

    def draw(self):
        if self.visible:
            x = self.x
            y = self.y
            width = self.width
            height = self.height
            if self.border_color:
                pygame.draw.rect(self.screen, self.border_color, (x, y, width, height), border_radius=self.border_radius)
                x += (self.border_size / 2)
                y += (self.border_size / 2)
                width -= self.border_size
                height -= self.border_size
            pygame.draw.rect(self.screen, self.color, (x, y, width, height), border_radius=self.border_radius)
            self.draw_text()

    def draw_text(self):
        screen_width, screen_height = self.screen.get_rect().size
        aspect_ratio = screen_width / screen_height

        text_size = min([(self.height / 2), (self.width / 2)])
        font_size = int(text_size * aspect_ratio)
        
        text_font = pygame.font.Font(Fonts.STAR_BORN.value, font_size)

        text_render = text_font.render(self.text, False, self.colors.foreground)
        text_width, text_height = text_render.get_rect().size
        x = self.x + ((self.width / 2) - (text_width / 2))
        y = self.y + ((self.height / 2) - (text_height / 2))
        
        if self.colors.foreground_border:
            border_text_render = text_font.render(self.text, False, self.colors.foreground_border)
            GraphicUtils.draw_text_border(self.screen, border_text_render, x, y, 3)

        self.screen.blit(text_render, (x, y))
