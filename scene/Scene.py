from pygame.event import Event

from typing import Tuple, Optional, Dict, Any
from enum import IntEnum

class SceneId(IntEnum):
    INVALID = -1
    HOME    =  0
    GAME    =  1

class Scene:
    def __init__(self):
        self.id = Scenes.INVALID
        
    def handle_event(self, event: Event) -> Tuple[int, Optional[Dict[Any, Any]]]:
        pass
