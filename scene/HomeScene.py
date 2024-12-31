from typing import Tuple, Optional, Dict, Any

import pygame
from pygame.surface import Surface
from pygame.event import Event

from Resources import Fonts
from Settings import ColorSettings
from Version import VERSION_STR
from scene.Scene import Scene, SceneId
from scene.SceneHandler import SceneSignals
from ui.Constants import UI_BUTTON_COLORS
from ui.Button import Button
from ui.CheckButton import CheckButton
from ui.Colors import Colors
from ui.NewGamePopup import NewGamePopup
from ui.Animator import Animator
from ui.AudioPlayer import AudioPlayer
from ui.MusicPlayer import MusicPlayer
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

        # Popup
        self.popup_new_game = NewGamePopup(self.screen, self)

    def create_buttons(self) -> None:
        button_width = self.width / 2
        button_height = 50
        x = (self.width / 2) - (button_width / 2)
        y = (self.height / 2) + (button_height / 2)
        play_button = Button(self.screen, (x, y), (button_width, button_height), "PLAY", UI_BUTTON_COLORS, self.handle_play_button)
        y += play_button.height + 10
        quit_button = Button(self.screen, (x, y), (button_width, button_height), "QUIT", UI_BUTTON_COLORS, self.handle_quit_button)
        self.buttons = [play_button, quit_button]

    def create_animations(self) -> None:
        self.subtitle_animator = Animator()
        subtitle_animation_values = { "x": (-self.subtitle_width, (self.width / 2)) }
        self.subtitle_animator.set_translate(self.draw_subtitle, subtitle_animation_values, 500)

        self.piece_one_animator = Animator()
        piece_one_animation_values = { "y": (-self.piece_size, (self.title_height - (self.title_height / 3))) }
        self.piece_one_animator.set_translate(self.draw_title_piece, piece_one_animation_values, 2000)

        self.piece_two_animator = Animator()
        piece_two_animation_values = { "y": (-self.piece_size, (self.title_height - (self.title_height / 4))) }
        self.piece_two_animator.set_translate(self.draw_title_piece, piece_two_animation_values, 2000)

        self.piece_one_animator.start()
        self.piece_two_animator.start()
        
    def handle_play_button(self) -> None:
        self.popup_new_game.show()
        
    def handle_quit_button(self) -> None:
        self.quit_clicked = True
        
    # @override
    def handle_event(self, event: Event) -> Tuple[int, Optional[Dict[Any, Any]]]:
        if self.play_clicked:
            data = {
                key: check_button.selected for key, check_button in self.popup_new_game.check_buttons.items()
            }
            self.play_clicked = False
            return SceneSignals.PLAY, data
        if self.quit_clicked:
            self.quit_clicked = False
            return SceneSignals.QUIT, None
        if self.popup_new_game.visible:
            self.popup_new_game.handle_event(event)
        else:
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

    def draw(self) -> None:       
        offset_x = self.title_width / 4
        GraphicUtils.draw_background(self.screen)
        self.piece_one_animator.animate(offset_x=offset_x, color=ColorSettings.player_one)
        offset_x += self.piece_size + 10
        self.piece_two_animator.animate(offset_x=offset_x, color=ColorSettings.player_two)
        self.draw_title()
        self.subtitle_animator.animate(offset_y=self.title_height)
        self.draw_version()
        for button in self.buttons:
            button.draw()
        self.popup_new_game.draw()

    def get_title_size(self) -> Tuple[float, float]:
        font_size = int(self.width / 8)
        title_font = pygame.font.Font(Fonts.STAR_BORN.value, font_size)
        text_render = title_font.render("Checkers", False, Colors.UI_RED.value)
        text_width, text_height = text_render.get_rect().size
        return text_width, text_height

    def get_subtitle_size(self) -> Tuple[float, float]:
        font_size = int(self.width / 8)
        subtitle_font = pygame.font.Font(Fonts.BLACK_BIRD.value, font_size)
        text_render = subtitle_font.render("Blitz", False, Colors.YELLOW.value)
        text_width, text_height = text_render.get_rect().size
        return text_width, text_height
       
    def draw_title(self) -> None:
        font_size = int(self.width / 8)
        title_font = pygame.font.Font(Fonts.STAR_BORN.value, font_size)
        text_render = title_font.render("Checkers", False, Colors.UI_RED.value)
        text_width, text_height = text_render.get_rect().size
        x = (self.width / 10)
        y = text_height
        border_text_render = title_font.render("Checkers", False, Colors.WHITE.value)
        GraphicUtils.draw_text_border(self.screen, border_text_render, x, y, 5)
        self.screen.blit(text_render, (x, y))

    def draw_title_piece(self, y: float, offset_x: float, color: Tuple[int, int, int]) -> None:
        x = (self.width / 10)
        GraphicUtils.draw_piece(self.screen, (x + offset_x, y), (self.piece_size, self.piece_size), color, outline_color=Colors.WHITE.value)

    def draw_subtitle(self, x: float, offset_y: float) -> None:
        font_size = int(self.width / 8)
        subtitle_font = pygame.font.Font(Fonts.BLACK_BIRD.value, font_size)
        text_render = subtitle_font.render("Blitz", False, Colors.YELLOW.value)
        text_width, text_height = text_render.get_rect().size
        y = text_height + offset_y
        border_text_render = subtitle_font.render("Blitz", False, Colors.WHITE.value)
        GraphicUtils.draw_text_border(self.screen, border_text_render, x, y, 5)
        self.screen.blit(text_render, (x, y))

    def draw_version(self) -> None:
        font_size = 20
        version_font = pygame.font.Font(Fonts.STAR_BORN.value, font_size)
        text_render = version_font.render(VERSION_STR, False, Colors.YELLOW.value)
        text_width, text_height = text_render.get_rect().size
        self.screen.blit(text_render, (self.width - text_width - 10, self.height - text_height - 10))
        
    def update(self) -> None:
        self.draw()
        if self.piece_one_animator.completed and self.piece_two_animator.completed:
            if not self.subtitle_animator.animating and not self.subtitle_animator.completed:
                AudioPlayer.play_speed_sound()
                self.subtitle_animator.start(delay_ms=250)
            elif self.subtitle_animator.completed:
                self.screen.fill(Colors.YELLOW.value)
                piece_one_animation_values = { "y": ((self.title_height - (self.title_height / 3)), (self.title_height - (self.title_height / 2))) }
                self.piece_one_animator.set_sine(self.draw_title_piece, piece_one_animation_values)
                self.piece_one_animator.start(delay_ms=100)

                piece_two_animation_values = { "y": ((self.title_height - (self.title_height / 4)), (self.title_height - (self.title_height / 5))) }
                self.piece_two_animator.set_sine(self.draw_title_piece, piece_two_animation_values)
                self.piece_two_animator.start(delay_ms=100)
                MusicPlayer.play()
