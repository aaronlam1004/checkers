from dataclasses import dataclass
from typing import Tuple, Callable

import pygame
from pygame.surface import Surface

@dataclass
class ButtonColors:
    background: Tuple[int, int, int]
    highlight: Tuple[int, int, int]
    text: Tuple[int, int, int]
    border: Tuple[int, int, int]
    

class Button:
    def __init__(self, screen: Surface, position: Tuple[int, int], dimension: Tuple[int, int],
                 text: str, button_colors: ButtonColors, on_click: Callable[[None], None]):
        self.screen = screen
        self.x, self.y = position
        self.width, self.height = dimension
        self.text = text

        self.colors = button_colors
        self.color = self.colors.background
        self.on_click = on_click

    def in_area(self, mouse_x: int, mouse_y: int):
        return mouse_x >= self.x and mouse_x <= self.x + self.width and mouse_y >= self.y and mouse_y <= self.y + self.height

    def hover(self, mouse_x: int, mouse_y: int):
        if self.in_area(mouse_x, mouse_y):
            self.color = self.colors.highlight
        else:
            self.color = self.colors.background

    def click(self, mouse_x: int, mouse_y: int):
        if self.in_area(mouse_x, mouse_y):
            self.on_click()

    def draw(self):
        pygame.draw.rect(self.screen, self.colors.border, (self.x, self.y, self.width, self.height), border_radius=3)
        border = 8
        pygame.draw.rect(self.screen, self.color, (self.x + (border / 2), self.y + (border / 2), self.width - border, self.height - border), border_radius=3)
        self.draw_text()

    def draw_text(self):
        screen_width, screen_height = self.screen.get_rect().size
        aspect_ratio = screen_width / screen_height

        text_size = min([(self.height / 2), (self.width / 2)])
        text_font = pygame.font.SysFont("Comic Sans MS", int(text_size * aspect_ratio))
        draw_text = text_font.render(self.text, False, self.colors.text)
        text_width, text_height = draw_text.get_rect().size
        x = self.x + ((self.width / 2) - (text_width / 2))
        y = self.y + ((self.height / 2) - (text_height / 2))
        self.screen.blit(draw_text, (x, y))
        
        
        
