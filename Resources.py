import os
import sys
from enum import Enum

import pygame

if getattr(sys, "frozen", False):
    BASE_PATH = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_PATH = os.path.dirname(__file__)

RESOURCE_PATH = os.path.join(BASE_PATH, "resources")
    
AUDIO = os.path.join(RESOURCE_PATH, "audio")
FONTS = os.path.join(RESOURCE_PATH, "fonts")
IMGS = os.path.join(RESOURCE_PATH, "imgs")

pygame.mixer.init()

class Sounds(Enum):
    MOVE = pygame.mixer.Sound(os.path.join(AUDIO, "move.wav"))
    SPEED = pygame.mixer.Sound(os.path.join(AUDIO, "speed.mp3"))

class Fonts(Enum):
    STAR_BORN  = os.path.join(FONTS, "Starborn.otf")
    BLACK_BIRD = os.path.join(FONTS, "Black Bird.otf")

class Images(Enum):
    KING       = os.path.join(IMGS, "king.png")
    HOME       = os.path.join(IMGS, "home.png")
    FLAG       = os.path.join(IMGS, "flag.png")
    REFRESH    = os.path.join(IMGS, "refresh.png")
    BACKGROUND = os.path.join(IMGS, "background.png")
    ICON       = os.path.join(IMGS, "icon.png")
