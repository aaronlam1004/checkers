from typing import Tuple, Callable

import pygame
from pygame.surface import Surface

from ui.Button import Button, ButtonColors

class IconButton(Button):
    def __init__(self, screen: Surface, position: Tuple[int, int], dimension: Tuple[int, int],
                 icon: str, button_colors: ButtonColors, on_click: Callable[[None], None],
                 visible: bool = True):
        self.icon = icon
        super().__init__(screen, position, dimension, "", button_colors, on_click, visible)

    def draw(self):
        super().draw()
        if self.visible:
            self.draw_icon()

    def draw_icon(self):
        icon_width = self.width / 1.5
        icon_height = self.height / 1.5
        icon_img = pygame.image.load(self.icon).convert_alpha()
        icon_img = pygame.transform.scale(icon_img, (icon_width, icon_height))
        icon_width, icon_height = icon_img.get_size()
        r, g, b = self.colors.foreground
        for row in range(icon_width):
            for col in range(icon_height):
                _, _, _, alpha = icon_img.get_at((row, col))
                icon_img.set_at((row, col), (r, g, b, alpha))
        icon_rect = (self.x + (icon_width / 4), self.y + (icon_width / 4), icon_width, icon_height)
        self.screen.blit(icon_img, icon_rect)
