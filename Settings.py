import os
import json
from typing import Tuple, Optional, Dict

from ui.Colors import Colors

SETTINGS_JSON = os.path.join(os.path.dirname(__file__), "settings.json")
MUSIC_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources", "music")

def rgb_to_hex(color: Tuple[int, int, int]) -> str:
    r, g, b = color
    return f"#{r:02x}{g:02x}{b:02x}"

def hex_to_rgb(color: str) -> Optional[Tuple[int, int, int]]:
    if len(color) != 7:
        return None
    if not color.startswith('#'):
        return None

    rgb_codes = []
    for i in range(1, len(color), 2):
        hex_code = color[i:i + 2]
        try:
            hex_value = int(hex_code, 16)
            rgb_codes.append(hex_value)
        except ValueError:
            print(f"Cannot interpret {hex_code} as a valid hex value")
    return tuple(rgb_codes)

class ColorSettings:
    player_one = Colors.UI_RED.value
    player_two = Colors.UI_BLACK.value
    white_tile = (236, 236, 208)
    black_tile = (114, 149, 81)
    selected_tile = (255, 235, 59)
    game_button = (255, 0, 0)
    game_button_icon = (255, 255, 255)

    @staticmethod
    def get_contrast_color(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        max_value = 0xFF
        r, g, b = color
        avg_value = (r + g + b) / 3
        if avg_value > (max_value / 2):
            return Colors.BLACK.value
        return Colors.WHITE.value

    @staticmethod
    def get_bg_color(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        max_value = 0xFF
        r, g, b = color
        avg_value = (r + g + b) / 3
        percent = 0.10
        if avg_value > (max_value / 2) or any([val == max_value for val in color]):
            r -= (max_value * percent)
            g -= (max_value * percent)
            b -= (max_value * percent)
        else:
            r += (max_value * percent)
            g += (max_value * percent)
            b += (max_value * percent)
        r = max_value if r > max_value else 0 if r < 0 else r
        g = max_value if g > max_value else 0 if g < 0 else g
        b = max_value if b > max_value else 0 if b < 0 else b
        return (int(r), int(g), int(b))

    @staticmethod
    def to_dict() -> Dict[str, str]:
        return {
            "player_one": rgb_to_hex(ColorSettings.player_one),
            "player_two": rgb_to_hex(ColorSettings.player_two),
            "white_tile": rgb_to_hex(ColorSettings.white_tile),
            "black_tile": rgb_to_hex(ColorSettings.black_tile),
            "selected_tile": rgb_to_hex(ColorSettings.selected_tile),
            "game_button": rgb_to_hex(ColorSettings.game_button),
            "game_button_icon": rgb_to_hex(ColorSettings.game_button_icon),
        }

class MusicSettings:
    directory = MUSIC_DIRECTORY

    @staticmethod
    def to_dict() -> Dict[str, str]:
        return { "directory": MusicSettings.directory }
    
class Settings:    
    @staticmethod
    def load() -> None:
        if os.path.exists(SETTINGS_JSON):
            try:
                with open(SETTINGS_JSON, 'r') as settings_json:
                    settings = json.loads(settings_json.read())
                if "color" in settings:
                    color_settings = settings["color"]
                    for color_key, color_value in color_settings.items():
                        if hasattr(ColorSettings, color_key):
                            rgb_color = hex_to_rgb(color_value)
                            if rgb_color:
                                setattr(ColorSettings, color_key, rgb_color)
                if "music" in settings:
                    music_settings = settings["music"]
                    for music_key, music_value in music_settings.items():
                        if hasattr(MusicSettings, music_key):
                            setattr(MusicSettings, music_key, music_value)
            except Exception as exception:
                print(f"Error occur loading settings: {exception}")
        else:
            Settings.export()
                
    @staticmethod
    def export() -> None:
        settings = {}
        settings["color"] = ColorSettings.to_dict()
        settings["music"] = MusicSettings.to_dict()
        with open(SETTINGS_JSON, 'w') as settings_file:
            settings_file.write(json.dumps(settings, indent=4))
