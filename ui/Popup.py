from typing import List

import pygame
from pygame.surface import Surface

from ui.Button import Button

class Popup:
    def __init__(self, screen: Surface, title: str = ""):
        self.visible = False
        self.screen = screen
        self.title = title
        self.buttons = []
        self.margin = 50
        self.screen_width, self.screen_height = self.screen.get_rect().size
        self.width = self.screen_width - (self.margin * 2)
        self.height = self.screen_height - (self.margin * 2)

    def set_title(self, title: str):
        self.title = title

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def handle_event(self, event):
        if self.visible:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.hide()

    def draw(self):
        if self.visible:
            self.draw_popup()

    def draw_popup(self):
        x = ((self.screen_width - self.width) / 2)
        y = ((self.screen_height - self.height) / 2)
        trans_surface = pygame.Surface((self.screen_width, self.screen_height))
        trans_surface.set_alpha(128)
        trans_surface.fill((0, 0, 0))
        self.screen.blit(trans_surface, (0, 0))
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, self.width, self.height), border_radius=20)
        for button in self.buttons:
            button.draw()

    def draw_title_border(self, text_render, x: float, y: float, border: float):
        self.screen.blit(text_render, (x - border, y))
        self.screen.blit(text_render, (x - border, y - border))
        self.screen.blit(text_render, (x - border, y + border))
        self.screen.blit(text_render, (x + border, y))
        self.screen.blit(text_render, (x + border, y - border))
        self.screen.blit(text_render, (x + border, y + border))
        self.screen.blit(text_render, (x, y - border))
        self.screen.blit(text_render, (x, y + border))
