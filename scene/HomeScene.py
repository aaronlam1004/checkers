from typing import Tuple

import pygame
from pygame.surface import Surface

from Resources import Fonts
from Settings import ColorSettings
from scene.Scene import Scene, SceneId
from scene.SceneHandler import SceneSignals
from ui.Constants import UI_BUTTON_COLORS
from ui.Button import Button
from ui.Colors import Colors
from ui.Animator import Animator
import ui.GraphicUtils as GraphicUtils

class HomeScene(Scene):
    def __init__(self, screen: Surface):
        self.id = SceneId.HOME
        self.screen = screen
        self.width, self.height = self.screen.get_rect().size
        self.piece_size = 175
        self.title_width, self.title_height = self.get_title_size()
        self.subtitle_width, self.subtitle_height = self.get_subtitle_size()
        self.create_buttons()

        # Signals
        self.play_clicked = False
        self.quit_clicked = False

        # Animations
        self.create_animations()

    def create_buttons(self):
        button_width = self.width / 2
        button_height = 50
        x = (self.width / 2) - (button_width / 2)
        y = (self.height / 2) + (button_height / 2)
        play_button = Button(self.screen, (x, y), (button_width, button_height), "PLAY", UI_BUTTON_COLORS, self.handle_play_button)
        y += play_button.height + 10
        quit_button = Button(self.screen, (x, y), (button_width, button_height), "QUIT", UI_BUTTON_COLORS, self.handle_quit_button)
        self.buttons = [play_button, quit_button]

    def create_animations(self):
        self.subtitle_animator = Animator()
        subtitle_animation_values = { "x": (-self.subtitle_width, (self.width / 2)) }
        self.subtitle_animator.set_translate(self.draw_subtitle, subtitle_animation_values, 1000)

        self.piece_one_animator = Animator()
        piece_one_animation_values = { "y": (-self.piece_size, (self.title_height - (self.title_height / 3))) }
        self.piece_one_animator.set_translate(self.draw_title_piece, piece_one_animation_values, 2000)

        self.piece_two_animator = Animator()
        piece_two_animation_values = { "y": (-self.piece_size, (self.title_height - (self.title_height / 3))) }
        self.piece_two_animator.set_translate(self.draw_title_piece, piece_two_animation_values, 2000)

        self.piece_one_animator.start()
        self.piece_two_animator.start()
        
    def handle_play_button(self):
        self.play_clicked = True
        
    def handle_quit_button(self):
        self.quit_clicked = True
        
    # @override
    def handle_event(self, event):
        if self.play_clicked:
            self.play_clicked = False
            return SceneSignals.PLAY, None
        if self.quit_clicked:
            self.quit_clicked = False
            return SceneSignals.QUIT, None
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.hover(mouse_x, mouse_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in self.buttons:
                button.click(mouse_x, mouse_y)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.handle_quit_button()
        return SceneSignals.NONE, None

    def draw(self):
        offset_x = self.title_width / 4
        self.screen.fill(Colors.BLACK.value)
        self.piece_one_animator.animate(offset_x=offset_x, color=ColorSettings.player_one)
        offset_x += self.piece_size + 10
        self.piece_two_animator.animate(offset_x=offset_x, color=ColorSettings.player_two)
        self.draw_title()
        self.subtitle_animator.animate(offset_y=self.title_height)
        for button in self.buttons:
            button.draw()

    def get_title_size(self):
        font_size = int(self.width / 8)
        title_font = pygame.font.Font(Fonts.STAR_BORN.value, font_size)
        text_render = title_font.render("Checkers", False, Colors.UI_RED.value)
        text_width, text_height = text_render.get_rect().size
        return text_width, text_height

    def get_subtitle_size(self):
        font_size = int(self.width / 8)
        subtitle_font = pygame.font.Font(Fonts.BLACK_BIRD.value, font_size)
        text_render = subtitle_font.render("Blitz", False, Colors.YELLOW.value)
        text_width, text_height = text_render.get_rect().size
        return text_width, text_height
       
    def draw_title(self):
        font_size = int(self.width / 8)
        title_font = pygame.font.Font(Fonts.STAR_BORN.value, font_size)
        text_render = title_font.render("Checkers", False, Colors.UI_RED.value)
        text_width, text_height = text_render.get_rect().size
        
        x = (self.width / 10)
        y = text_height

        border_text_render = title_font.render("Checkers", False, Colors.WHITE.value)
        GraphicUtils.draw_text_border(self.screen, border_text_render, x, y, 5)
        self.screen.blit(text_render, (x, y))

    def draw_title_piece(self, y: float, offset_x: float, color: Tuple[int, int, int]):
        x = (self.width / 10)
        GraphicUtils.draw_piece(self.screen, (x + offset_x, y), (self.piece_size, self.piece_size), color, outline_color=Colors.WHITE.value)

    def draw_subtitle(self, x: float, offset_y: float):
        font_size = int(self.width / 8)
        subtitle_font = pygame.font.Font(Fonts.BLACK_BIRD.value, font_size)
        text_render = subtitle_font.render("Blitz", False, Colors.YELLOW.value)
        text_width, text_height = text_render.get_rect().size
        y = text_height + offset_y
        border_text_render = subtitle_font.render("Blitz", False, Colors.WHITE.value)
        GraphicUtils.draw_text_border(self.screen, border_text_render, x, y, 5)
        self.screen.blit(text_render, (x, y))
        
    def update(self):
        self.draw()
        if self.piece_one_animator.completed and self.piece_two_animator.completed:
            if not self.subtitle_animator.animating and not self.subtitle_animator.completed:
                self.subtitle_animator.start()
        
