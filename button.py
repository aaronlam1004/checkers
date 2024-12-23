from graphics import *
from events import *

class Button:
    def __init__(self, x, y, width, height, text, color, highlight_color, on_click):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.base_color = color
        self.highlight_color = highlight_color
        self.color = self.base_color
        self.button_area = (x, x + width, y, y + height)
        self.on_click = on_click
        
    def check_in_area(self):
        if is_in_button_area(self.button_area):
            self.color = self.highlight_color
            return True
        self.color = self.base_color
        return False
