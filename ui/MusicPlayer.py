import os
import glob

import random
import pygame

from Settings import MusicSettings

class MusicPlayer:
    tracks = []
    queue = []
    music_channel = pygame.mixer.find_channel()
    playing = False
    
    @staticmethod
    def load() -> None:
        MusicPlayer.music_channel.pause()
        music_dir = MusicSettings.directory
        if os.path.exists(music_dir) and os.path.isdir(music_dir):
            MusicPlayer.tracks = [pygame.mixer.Sound(music) for music in glob.glob(f"{music_dir}/*.mp3")]
            MusicPlayer.queue = MusicPlayer.tracks.copy()

    @staticmethod
    def play() -> None:
        MusicPlayer.music_channel.set_volume(0.35)
        MusicPlayer.play_next_song()
        MusicPlayer.playing = True

    @staticmethod
    def check() -> None:
        if not MusicPlayer.music_channel.get_busy():
            if len(MusicPlayer.queue) == 0 and len(MusicPlayer.tracks) > 0:
                MusicPlayer.queue = MusicPlayer.tracks.copy()
            MusicPlayer.play_next_song()

    @staticmethod
    def play_next_song() -> None:
        if len(MusicPlayer.queue) > 0:
            index = random.randint(0, len(MusicPlayer.queue) - 1)
            track = MusicPlayer.queue.pop(index)
            MusicPlayer.music_channel.play(track)

    @staticmethod
    def reload() -> None:
        MusicPlayer.load()
        MusicPlayer.play()
