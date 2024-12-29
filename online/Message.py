from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class Message:
    piece: Tuple[int, int]
    move: Tuple[int, int]
    capture: Optional[Tuple[int, int]]

    def to_dict(self):
        return {
            "piece": self.piece,
            "move": self.move,
            "capture": self.capture
        }
