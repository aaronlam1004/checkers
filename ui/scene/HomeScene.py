import pygame
from pygame.surface import Surface

from ui.scene.Scene import Scene, SceneId
from ui.EventHandler import Signals
from ui.Button import Button, ButtonColors

class HomeScene(Scene):
    def __init__(self, screen: Surface):
        self.id = SceneId.HOME
        self.screen = screen
        self.width, self.height = self.screen.get_rect().size
        self.init_buttons()

        # Signals
        self.play_clicked = False
        self.quit_clicked = False

    def init_buttons(self):
        button_width = self.width / 2
        button_height = 50
        x = (self.width / 2) - (button_width / 2)
        y = (self.height / 2) - (button_height / 2)

        play_button_colors = ButtonColors(
            (255, 0, 0),
            (0, 0, 0),
            highlight=(0, 0, 255),
            border=(255, 255, 255),
            text_border=(255, 255, 255)
        )
        play_button = Button(self.screen, (x, y), (button_width, button_height), "PLAY", play_button_colors, self.handle_play)
        
        y += button_height + 10
        quit_button_colors = ButtonColors(
            (255, 0, 0),
            (0, 0, 0),
            highlight=(0, 0, 255),
            border=(255, 255, 255),
            text_border=(255, 255, 255)
        )
        quit_button = Button(self.screen, (x, y), (button_width, button_height), "QUIT", quit_button_colors, self.handle_quit)
        
        self.buttons = [play_button, quit_button]

    def handle_play(self):
        self.play_clicked = True
        
    def handle_quit(self):
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

        if self.play_clicked:
            self.play_clicked = False
            return Signals.PLAY, None
        elif self.quit_clicked:
            self.quit_clicked = False
            return Signals.QUIT, None
        return Signals.NONE, None

    def draw(self):
        self.screen.fill((40, 40, 40))
        for button in self.buttons:
            button.draw()
        
    def update(self):
        self.draw()
        
