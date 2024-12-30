import pygame
import random
from enum import IntEnum

from HotLoader import HotLoader
from Settings import Settings, SETTINGS_JSON

from board.StandardBoard import StandardBoard

from scene.Scene import SceneId
from scene.HomeScene import HomeScene
from scene.GameScene import GameScene
from scene.SceneHandler import SceneHandler, SceneSignals
from ui.Window import Window
from ui.MusicPlayer import MusicPlayer

if __name__ == "__main__":
    Settings.load()
    MusicPlayer.load()
    
    HotLoader.add_file(SETTINGS_JSON, Settings.load)
    HotLoader.add_callback(SETTINGS_JSON, MusicPlayer.reload)
    
    window = Window((800, 700), "Checkers Blitz")
    home_scene = HomeScene(window.screen)
    game_scene = None

    SceneHandler.set_scene(home_scene)
    
    while True:
        HotLoader.check()
        if MusicPlayer.playing:
            MusicPlayer.check()       
        signal_id, data = SceneHandler.handle_events()
        if signal_id == SceneSignals.QUIT:
            break
        elif signal_id == SceneSignals.PLAY:
            flipped = random.choice([True, False])
            board = StandardBoard(flipped=flipped)
            board.setup()
            if data.get("blitz", True):
                board.enable_blitz_mode()
            if data.get("force_capture", False):
                board.enable_force_capture()
            if data.get("all_kings", False):
                board.enable_all_kings_mode()
            game_scene = GameScene(window.screen, board, flipped=flipped)
            SceneHandler.set_scene(game_scene)
        elif signal_id == SceneSignals.HOME:
            game_scene = None
            SceneHandler.set_scene(home_scene)

        scene_id = SceneHandler.scene.id
        if scene_id == SceneId.HOME:
            home_scene.update()
        elif scene_id == SceneId.GAME:
            game_scene.update()
        window.update()
