from enum import IntEnum

class SceneId(IntEnum):
    INVALID = -1
    HOME    =  0
    GAME    =  1

class Scene:
    def __init__(self):
        self.id = Scenes.INVALID
        
    def handle_event(self):
        pass
