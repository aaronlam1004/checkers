from dataclasses import dataclass
from typing import List, Callable

import os

@dataclass
class HotLoadFile:
    f: str
    timestamp: int
    callbacks: List[Callable[[None], None]]

class HotLoader:
    files = {}
    
    @staticmethod
    def add_file(f: str, update_callback: Callable[[None], None]) -> None:
        timestamp = None
        if os.path.exists(f):
            timestamp = os.stat(f).st_mtime
        HotLoader.files[f] = HotLoadFile(f, timestamp, [update_callback])

    @staticmethod
    def remove_file(f: str) -> None:
        if f in files:
            del files[f]

    @staticmethod
    def add_callback(f: str, update_callback: Callable[[None], None]) -> None:
        if f in HotLoader.files:
            HotLoader.files[f].callbacks.append(update_callback)

    @staticmethod
    def pop_callback(f: str) -> None:
        if f in HotLoader.files:
            if len(Hotloader.files[f].callbacks) > 1:
                HotLoader.files[f].callbacks.pop()
    
    @staticmethod
    def check() -> None:
        for f in HotLoader.files:
            if os.path.exists(f):
                modified_time = os.stat(f).st_mtime
                if modified_time != HotLoader.files[f].timestamp:
                    print("Change detected, reloading...")
                    HotLoader.files[f].timestamp = modified_time
                    for callback in HotLoader.files[f].callbacks:
                        callback()
