import pygame

from Resources import *

class AudioPlayer:
    @staticmethod
    def play_piece_move():
        Sounds.MOVE.value.play()
