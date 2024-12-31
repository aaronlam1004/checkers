from typing import Optional, Callable, Tuple, Optional, Dict, Any
from enum import IntEnum

import pygame

from scene.Scene import Scene

class SceneSignals(IntEnum):
    QUIT = -1
    NONE = 0
    PLAY = 1
    HOME = 2

class SceneHandler:
    scene = None

    @staticmethod
    def set_scene(scene: Scene) -> None:
        SceneHandler.scene = scene
    
    @staticmethod
    def handle_events() -> Tuple[int, Optional[Dict[Any, Any]]]:
        event_data = None
        event_signal = SceneSignals.NONE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return SceneSignals.QUIT, None
            if SceneHandler.scene is not None:
                signal_id, signal_data = SceneHandler.scene.handle_event(event)
                if signal_id != SceneSignals.NONE:
                    event_signal = signal_id
                    event_data = signal_data
        return event_signal, event_data
