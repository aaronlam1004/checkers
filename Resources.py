import os
from enum import Enum

import pygame

RESOURCE_PATH = os.path.join(os.path.dirname(__file__), "resources")
AUDIO = os.path.join(RESOURCE_PATH, "audio")
FONTS = os.path.join(RESOURCE_PATH, "fonts")
IMGS = os.path.join(RESOURCE_PATH, "imgs")

pygame.mixer.init()

class Sounds(Enum):
    MOVE = pygame.mixer.Sound(os.path.join(AUDIO, "move.wav"))


class Fonts(Enum):
    STAR_BORN = os.path.join(FONTS, "Starborn.otf")

class Images(Enum):
    KING = os.path.join(IMGS, "king.png")
