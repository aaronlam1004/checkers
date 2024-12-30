import pygame

from Resources import Sounds

class AudioPlayer:
    @staticmethod
    def play_checker_sound():
        Sounds.MOVE.value.play()

    @staticmethod
    def play_speed_sound():
        Sounds.SPEED.value.play()
