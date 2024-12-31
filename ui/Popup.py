from typing import List, Tuple
from dataclasses import dataclass

import pygame
from pygame.surface import Surface
from pygame.event import Event

from ui.Button import Button
from ui.Colors import Colors

@dataclass
class PopupColors:
    background: Tuple[int, int, int] = Colors.BLACK.value
    foreground: Tuple[int, int, int] = Colors.WHITE.value,
    border: Tuple[int, int, int] = Colors.WHITE.value

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
        self.x = (self.screen_width - self.width) / 2
        self.y = (self.screen_height - self.height) / 2
        self.colors = PopupColors()
        self.border_size = border_size

    def set_title(self, title: str) -> None:
        self.title = title

    def show(self) -> None:
        self.visible = True

    def hide(self) -> None:
        self.visible = False

    def handle_event(self, event: Event) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.visible:
            if event.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    button.hover(mouse_x, mouse_y)
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    button.click(mouse_x, mouse_y)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.hide()

    def draw(self) -> None:
        if self.visible:
            self.draw_background()
            self.draw_popup()

    def draw_background(self) -> None:
        trans_surface = pygame.Surface((self.screen_width, self.screen_height))
        trans_surface.set_alpha(128)
        trans_surface.fill(Colors.BLACK.value)
        self.screen.blit(trans_surface, (0, 0))
            
    def draw_popup(self) -> None:
        x = self.x
        y = self.y
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
