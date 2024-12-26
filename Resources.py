import os
from enum import Enum

import pygame

RESOURCE_PATH = os.path.join(os.path.dirname(__file__), "resources")
AUDIO = os.path.join(RESOURCE_PATH, "audio")

pygame.mixer.init()

class Sounds(Enum):
    MOVE = pygame.mixer.Sound(os.path.join(AUDIO, "move.wav"))
