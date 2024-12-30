from typing import Tuple

import pygame

from Resources import Images

class Window:
    def __init__(self, dimensions: Tuple[int, int], title: str):
        self.width, self.height = dimensions
        self.screen = pygame.display.set_mode(dimensions)
        self.set_title(title)
        pygame.font.init()
        self.icon = pygame.image.load(Images.ICON.value)
        pygame.display.set_icon(self.icon)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def set_title(self, title: str):
        self.title = title
        pygame.display.set_caption(self.title)

    def update(self):
        pygame.display.update()
