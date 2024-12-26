from typing import Optional, Callable
from enum import IntEnum

import pygame

from ui.scene.Scene import Scene

class Signals(IntEnum):
    QUIT = -1
    NONE = 0
    PLAY = 1

class EventHandler:
    scene = None

    @staticmethod
    def set_scene(scene: Scene):
        EventHandler.scene = scene
    
    @staticmethod
    def handle_events():
        event_data = None
        event_signal = Signals.NONE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Signals.QUIT, None
            if EventHandler.scene is not None:
                signal_id, signal_data = EventHandler.scene.handle_event(event)
                if signal_id != Signals.NONE:
                    event_signal = signal_id
                    event_data = signal_data
        return event_signal, event_data
