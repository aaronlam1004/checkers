from typing import Tuple

import pygame

class Window:
    def __init__(self, dimensions: Tuple[int, int], title: str):
        self.title = title
        self.width, self.height = dimensions
        self.screen = pygame.display.set_mode(dimensions)
        pygame.font.init()
        pygame.display.set_caption(self.title)

    @staticmethod
    def update():
        pygame.display.update()
