import os
import json
from typing import Tuple

from ui.Colors import Colors

SETTINGS_JSON = os.path.join(os.path.dirname(__file__), "settings.json")

class ColorSettings:
    player_one = (183, 63, 52)
    player_two = (43, 42, 63)
    white_tile = (236, 236, 208)
    black_tile = (114, 149, 81)
    selected_tile = (255, 235, 59)
    game_button = (255, 0, 0)
    game_button_icon = (255, 255, 255)

    @staticmethod
    def get_contrast_color(color: Tuple[int, int, int]):
        max_value = 0xFF
        r, g, b = color
        avg_value = (r + g + b) / 3
        if avg_value > (max_value / 2):
            return Colors.BLACK.value
        return Colors.WHITE.value

    @staticmethod
    def get_bg_color(color: Tuple[int, int, int]):
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

class Settings:
    @staticmethod
    def rgb_to_hex(color: Tuple[int, int, int]):
        r, g, b = color
        return f"#{r:02x}{g:02x}{b:02x}"

    def hex_to_rgb(color: str):
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
                
    
    @staticmethod
    def load():
        if os.path.exists(SETTINGS_JSON):
            try:
                with open(SETTINGS_JSON, 'r') as settings_json:
                    settings = json.loads(settings_json.read())
                if "color" in settings:
                    color_settings = settings["color"]
                    for color_key, color in color_settings.items():
                        if hasattr(ColorSettings, color_key):
                            rgb_color = Settings.hex_to_rgb(color)
                            if rgb_color:
                                setattr(ColorSettings, color_key, rgb_color)
            except Exception as exception:
                print(f"Error occur loading settings: {exception}")
                

# def create_settings(widgets, keys):
#     settings = {}
#     i = 0
#     for k in keys:
#         if i != 5 and i != 9:
#             settings[k] = widgets[i]["bg"]
#         else:
#             settings[k] = widgets[i]["text"]
#         i += 1
#     with open(SETTINGS_JSON, 'w') as outfile:
#         json.dump(settings, outfile)
#     messagebox.showinfo(title="Settings file written", message="Settings file has been sucessfully written")
#     load_graphics_settings()
# 
# def select_image(widget):
#     valid_files = [
#         ("PNG", "*.png"),
#         ("JPG", "*.jpg"),
#         ("JPEG", "*.jpeg"),
#         ("PGM", "*.pgm"),
#         ("PPM", "*.ppm"),
#         ("BMP", "*.bmp")
#     ]
#     file = tkinter.filedialog.askopenfile(initialdir="./",filetypes=valid_files)
#     if file != None:
#         image = Image.open(file.name)
#         image = image.resize((40, 40))
#         king = ImageTk.PhotoImage(image)
#         widget.config(image=king, text=file.name)
#         widget.photo = king
# 
# def reset_options(root, opt):
#     try:
#         os.remove(SETTINGS_JSON)
#     except:
#         pass
#     messagebox.showinfo(title="Settings file reset", message="Settings file has been successfully reset")
#     root.destroy()
#     root.__init__()
#     main(root)
# 
# def main(root):
#     load_graphics_settings()
#     root.title("Checkers Settings")
#     try:
#         with open(SETTINGS_JSON, 'r') as settings:
#             options = json.load(settings)
#     except:
#         options = {
#             "bwhite": rgb_to_html((227, 182, 84)),
#             "bblack": rgb_to_html((179, 142, 64)),
#             "p1bg": rgb_to_html((235, 106, 106)),
#             "p1fg": rgb_to_html((186, 63, 52)),
#             "p1king": rgb_to_html((140, 14, 0)),
#             "p1image": "./resources/king.png",
#             "p2bg": rgb_to_html((61, 60, 56)),
#             "p2fg": rgb_to_html((43, 42, 40)),
#             "p2king": rgb_to_html((0, 0, 0)),
#             "p2image": "./resources/king.png",
#             "turn": rgb_to_html((255, 255, 0))
#         }
# 
#     fontstyle = tkinter.font.Font(family="Lucida Grande", size=15)
#     title = tkinter.Label(text="Checker Settings", font=fontstyle)
#     title.grid(row=1, column=2, pady=5)
# 
#     labels = ["Board (WHITE)", "Board (BLACK)", 
#               "P1 (BG)", "P1 (FG)", "P1 (KING)", "P1 (KING)", 
#               "P2 (BG)", "P2 (FG)", "P2 (KING)", "P2 (KING)", 
#               "TURN"]
# 
#     while True:
#         try:
#             modifiers = []
#             padding = (120, 0)
#             i = 0
#             for k, v in options.items():
#                 label = tkinter.Label(root, text=labels[i])
# 
#                 if i != 5 and i != 9:
#                     modifier = tkinter.Button(root, text="    ", bg=v)
#                     modifier["command"] = lambda arg=modifier: choose_color(arg)
#                 else:
#                     image = Image.open(v)
#                     image = image.resize((40, 40))
#                     king = ImageTk.PhotoImage(image)
#                     modifier = tkinter.Button(image=king, text=v)
#                     modifier["command"] = lambda arg=modifier: select_image(arg)
#                     modifier.photo = king
# 
#                 modifiers.append(modifier)
#                 label.grid(row=i+2, column=1, padx=padding)
#                 modifier.grid(row=i+2, column=2, pady=5)
#                 i += 1
#             break
#         except:
#             os.remove(SETTINGS_JSON)
#             options = {
#                 "bwhite": rgb_to_html((227, 182, 84)),
#                 "bblack": rgb_to_html((179, 142, 64)),
#                 "p1bg": rgb_to_html((235, 106, 106)),
#                 "p1fg": rgb_to_html((186, 63, 52)),
#                 "p1king": rgb_to_html((140, 14, 0)),
#                 "p1image": "./resources/king.png",
#                 "p2bg": rgb_to_html((61, 60, 56)),
#                 "p2fg": rgb_to_html((43, 42, 40)),
#                 "p2king": rgb_to_html((0, 0, 0)),
#                 "p2image": "./resources/king.png",
#                 "turn": rgb_to_html((255, 255, 0))
#             }
#             
#     create_button = tkinter.Button(root, text="Write settings file", command=lambda a=modifiers, b=options.keys(): create_settings(a, b))
#     create_button.grid(row=i+2, column=2)
#     reset_button = tkinter.Button(root, text="Reset to default", command=lambda a=root, b=options: reset_options(a, b), bg="#FF3333")
#     reset_button.grid(row=i+3, column=1)
# 
#     root.geometry("500x550")
#     root.mainloop()
# 
# if __name__ == "__main__":
#     root = tkinter.Tk()
#     main(root)
