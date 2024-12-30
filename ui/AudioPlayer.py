import pygame

from Resources import Sounds

class AudioPlayer:
    @staticmethod
    def play_checker_sound():
        Sounds.MOVE.value.play()
