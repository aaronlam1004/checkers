import pygame
from enum import IntEnum

# from checkers import Canvas, Checkers
# from home import Home
# from graphics import *
# from events import *

# from board.Board import * 
from board.StandardBoard import StandardBoard

from ui.Window import Window
from ui.scene.Scene import SceneId
from ui.scene.HomeScene import HomeScene
from ui.scene.GameScene import GameScene
from ui.EventHandler import EventHandler, Signals

if __name__ == "__main__":
    window = Window((800, 700), "Checkers")
    home_scene = HomeScene(window.screen)
    game_scene = None
    # game_scene = GameScene(window.screen, board)

    EventHandler.set_scene(home_scene)
    
    while True:
        signal_id, data = EventHandler.handle_events()
        if signal_id == Signals.QUIT:
            break
        elif signal_id == Signals.PLAY:
            board = StandardBoard()
            board.setup()
            # board.set_size(10)
            board.enable_blitz_mode()
            game_scene = GameScene(window.screen, board)
            EventHandler.set_scene(game_scene)
        elif signal_id == Signals.HOME:
            game_scene = None
            EventHandler.set_scene(home_scene)

        scene_id = EventHandler.scene.id
        if scene_id == SceneId.HOME:
            home_scene.update()
        elif scene_id == SceneId.GAME:
            game_scene.update()
        window.update()
    # checkers = Checkers(canvas)
    # home = Home(canvas, checkers)
    # home.show()
