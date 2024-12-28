from typing import Tuple

import pygame
from pygame.surface import Surface

from Resources import Fonts
from Settings import ColorSettings
from scene.Scene import Scene, SceneId
from scene.SceneHandler import SceneSignals
from ui.Button import Button, ButtonColors

class HomeScene(Scene):
    def __init__(self, screen: Surface):
        self.id = SceneId.HOME
        self.screen = screen
        self.width, self.height = self.screen.get_rect().size
        self.create_buttons()

        # Signals
        self.play_clicked = False
        self.quit_clicked = False

        # Animation
        self.piece_one_y = 0
        self.piece_two_y = 0

    def create_buttons(self):
        button_width = self.width / 2
        button_height = 50
        x = (self.width / 2) - (button_width / 2)
        y = (self.height / 2) - (button_height / 2)

        play_button_colors = ButtonColors(
            (235, 106, 106),
            (43, 42, 40),
            highlight=(186, 63, 52),
            border=(255, 255, 255),
            foreground_border=(255, 255, 255)
        )
        play_button = Button(self.screen, (x, y), (button_width, button_height), "PLAY", play_button_colors, self.handle_play_button)
        
        y += button_height + 10
        quit_button_colors = ButtonColors(
            (235, 106, 106),
            (43, 42, 40),
            highlight=(186, 63, 52),
            border=(255, 255, 255),
            foreground_border=(255, 255, 255)
        )
        quit_button = Button(self.screen, (x, y), (button_width, button_height), "QUIT", quit_button_colors, self.handle_quit_button)
        
        self.buttons = [play_button, quit_button]

    def handle_play_button(self):
        self.play_clicked = True
        
    def handle_quit_button(self):
        self.quit_clicked = True
        
    # @override
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in self.buttons:
                button.hover(mouse_x, mouse_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in self.buttons:
                button.click(mouse_x, mouse_y)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.handle_quit_button()

        if self.play_clicked:
            self.play_clicked = False
            return SceneSignals.PLAY, None
        elif self.quit_clicked:
            self.quit_clicked = False
            return SceneSignals.QUIT, None
        return SceneSignals.NONE, None

    def draw(self):
        self.screen.fill((20, 20, 20))
        self.draw_title()
        for button in self.buttons:
            button.draw()
       
    def draw_title(self):
        font_size = int(self.width / 8)
        title_font = pygame.font.Font(Fonts.STAR_BORN.value, font_size)
        text_render = title_font.render("Checkers", False, (235, 106, 106))
        text_width, text_height = text_render.get_rect().size
        
        x = (self.width / 10)
        y = text_height
        
        piece_one_final_y = y - (text_height / 3)
        piece_two_final_y = y - (text_height / 4)
        
        if self.piece_one_y > piece_one_final_y:
            self.piece_one_y = piece_one_final_y
        if self.piece_two_y > piece_two_final_y:
            self.piece_two_y = piece_two_final_y
        
        self.draw_piece(x + (text_width / 4), self.piece_one_y, ColorSettings.player_one)
        self.draw_piece(x + (text_width / 4) + 185, self.piece_two_y, ColorSettings.player_two)

        border_text_render = title_font.render("Checkers", False, (255, 255, 255))
        self.draw_title_border(border_text_render, x, y, 5)
        self.screen.blit(text_render, (x, y))

    def draw_piece(self, x: float, y: float, color: Tuple[int, int, int]):
        piece_width, piece_height = (175, 175)
        pygame.draw.ellipse(self.screen, (255, 255, 255), (x, y, piece_width, piece_height))
        border = 10
        x += (border / 2)
        y += (border / 2)
        piece_width -= border
        piece_height -= border
        color_bg = ColorSettings.get_bg_color(color)
        pygame.draw.ellipse(self.screen, color_bg, (x, y, piece_width, piece_height))
        margin = 20
        x += (margin / 2)
        y += (margin / 2)
        piece_width -= margin
        piece_height -= margin
        pygame.draw.ellipse(self.screen, color, (x, y, piece_width, piece_height))

    def draw_title_border(self, text_render, x: float, y: float, border: float):
        self.screen.blit(text_render, (x - border, y))
        self.screen.blit(text_render, (x - border, y - border))
        self.screen.blit(text_render, (x - border, y + border))
        self.screen.blit(text_render, (x + border, y))
        self.screen.blit(text_render, (x + border, y - border))
        self.screen.blit(text_render, (x + border, y + border))
        self.screen.blit(text_render, (x, y - border))
        self.screen.blit(text_render, (x, y + border))
        
        
    def update(self):
        self.draw()
        self.piece_one_y += 0.5
        self.piece_two_y += 0.5
        
