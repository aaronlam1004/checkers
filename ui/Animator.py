import math
import time

import pygame

from typing import Any, Callable, Dict, Tuple

class Animator:
    def __init__(self):
        self.animating = False
        self.draw_method = None
        self.values = {}
        self.animation_values = {}
        self.completed = False
        self.start_time_ms = 0
        self.delay_ms = 0

    def set_translate(self, draw_method: Callable,
                      animation_values: Dict[str, Tuple[float, float]],
                      time_ms: float,
                      loop: bool = False):
        self.loop = loop
        self.draw_method = draw_method
        self.animation_values = animation_values
        self.values = {}
        self.increments = {}
        for arg, anim_range in animation_values.items():
            start_value, end_value = anim_range
            self.values[arg] = start_value
            self.increments[arg] = lambda x: x + ((end_value - start_value) / (time_ms / 10))
        self.completed = False

    def set_sine(self, draw_method: Callable,
                 animation_values: Dict[str, Tuple[float, float]]):
        self.loop = True
        self.draw_method = draw_method
        self.animation_values = animation_values
        self.values = {}
        for arg, anim_range in animation_values.items():
            start_value, end_value = anim_range
            self.values[arg] = start_value
            a = (end_value - start_value) / 2
            c = end_value - a
            self.increments[arg] = lambda x: (a * math.sin(3 * time.time())) + c
        self.completed = False

    def start(self, delay_ms: float = 0):
        self.animating = True
        self.delay_ms = delay_ms
        self.start_time_ms = time.time() * 1000

    def stop(self):
        self.animating = False
        
    def animate(self, **kwargs):
        now = time.time() * 1000
        if now - self.start_time_ms > self.delay_ms:
            if self.animating and self.draw_method:
                for arg in self.values:
                    anim_range = self.animation_values.get(arg, None)
                    increment = self.increments.get(arg, 0)
                    if anim_range:
                        start_value, end_value = anim_range
                        value = self.values[arg]
                        if (start_value < end_value and value >= end_value) or (start_value > end_value and value <= end_value):
                            if self.loop:
                                self.values[arg] = start_value
                            else:
                                self.values[arg] = end_value
                                self.completed = True
                                self.stop()
                        else:
                            self.values[arg] = increment(value)
        args_dict = {}
        args_dict.update(self.values)
        args_dict.update(kwargs)
        self.draw_method(**args_dict)
