import socket
import pygame
import tkinter

import settings
import online.online as online
from checkers import Checkers
from button import Button
from graphics import *
from events import *

class Home:
    def __init__(self, canvas, checkers):
        self.canvas = canvas
        self.width = canvas.width
        self.height = canvas.height
        self.aspect_ratio = self.height / self.width
        self.checkers = checkers
        self.running = False

    def handle_events(self, buttons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    if button.check_in_area():
                        button.on_click()
            elif event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    button.check_in_area()

    def handle_play(self):
        self.running = False
        self.checkers.play_local()

    def handle_online(self):
        root = tkinter.Tk()
        online.main(root)

    def handle_settings(self):
        root = tkinter.Tk()
        settings.main(root)

    def handle_quit(self):
        self.running = False

    def show(self):
        button_color = (247, 103, 54)
        highlight_color = (81, 237, 122)
        screen = self.canvas.screen
        fontsize = int(100 * self.aspect_ratio)

        bfontsize = int(fontsize / 5)
        buttonfont = pygame.font.SysFont("Comic Sans MS", bfontsize)
        
        bwidth = 200 * self.aspect_ratio
        bheight = 50 * self.aspect_ratio
        
        bx = self.width / 2 - (bwidth / 2)
        by = self.height / 2
        bpadding = 5
        
        buttons = [
            Button(bx, by, bwidth, bheight, "PLAY", (247, 103, 54), (81, 237, 122), self.handle_play),
            Button(bx, by + bheight + bpadding, bwidth, bheight, "ONLINE", (247, 103, 54), (81, 237, 122), self.handle_online),
            Button(bx, by + (2 * bheight) + (2 * bpadding), bwidth, bheight, "SETTINGS", (247, 103, 54), (81, 237, 122), self.handle_settings),
            Button(bx, by + (3 * bheight) + (3 * bpadding), bwidth, bheight, "QUIT", (247, 103, 54), (81, 237, 122), self.handle_quit)
        ]

        self.running = True
        while self.running:
            # Handle events
            self.handle_events(buttons)
            
            # Background
            screen.fill((255, 255, 255))
            
            # Title
            titlefont = pygame.font.SysFont("Comic Sans MS", fontsize)
            textsurface = titlefont.render("Checkers", False, (0, 0, 0))
            twidth, theight = textsurface.get_rect().size
            x = self.width / 2 - (twidth / 2)
            y = self.height / 4 - (theight / 2)
            screen.blit(textsurface, (x, y))

            # Buttons
            for b in buttons:
                draw_button(screen, b.text, buttonfont, (0, 0, 0), (b.x, b.y), (b.width, b.height), b.color)
                
            self.canvas.update()

        pygame.quit()
