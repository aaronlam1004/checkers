from typing import List, Tuple
from dataclasses import dataclass

import pygame
from pygame.surface import Surface

from ui.Button import Button

@dataclass
class PopupColors:
    background: Tuple[int, int, int] = (20, 20, 20)
    foreground: Tuple[int, int, int] = (255, 255, 255)
    border: Tuple[int, int, int] = (255, 255, 255)

class Popup:
    def __init__(self, screen: Surface, title: str = "", border_size: int = 16):
        self.visible = False
        self.screen = screen
        self.title = title
        self.buttons = []
        self.margin = 50
        self.screen_width, self.screen_height = self.screen.get_rect().size
        self.width = self.screen_width - (self.margin * 2)
        self.height = (self.screen_height / 2) - (self.margin * 2)
        self.colors = PopupColors()
        self.border_size = border_size

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
            self.draw_background()
            self.draw_popup()

    def draw_background(self):
        trans_surface = pygame.Surface((self.screen_width, self.screen_height))
        trans_surface.set_alpha(128)
        trans_surface.fill((0, 0, 0))
        self.screen.blit(trans_surface, (0, 0))
            
    def draw_popup(self):
        x = ((self.screen_width - self.width) / 2)
        y = ((self.screen_height - self.height) / 2)
        width = self.width
        height = self.height
        if self.border_size > 0:
            pygame.draw.rect(self.screen, (255, 255, 255), (x, y, width, height), border_radius=20)
            x += (self.border_size / 2)
            y += (self.border_size / 2)
            width -= self.border_size
            height -= self.border_size
        pygame.draw.rect(self.screen, self.colors.background, (x, y, width, height), border_radius=20)
        for button in self.buttons:
            button.draw()
