import pygame

from Resources import Sounds

class AudioPlayer:
    @staticmethod
    def play_checker_sound() -> None:
        Sounds.MOVE.value.play()

    @staticmethod
    def play_speed_sound() -> None:
        Sounds.SPEED.value.play()
