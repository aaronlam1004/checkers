import tkinter
import tkinter.font
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageTk
import json
import os
from graphics import *

SETTINGS_JSON = os.path.join(os.path.dirname(__file__), "settings.json")

def choose_color(widget):
    color_code = colorchooser.askcolor(title="Color")
    widget["bg"] = color_code[1]

def rgb_to_html(rgb):
    r, g, b = rgb
    return "#" + str(format(r, "02x")) +str(format(g, "02x")) + str(format(b, "02x"))

def create_settings(widgets, keys):
    settings = {}
    i = 0
    for k in keys:
        if i != 5 and i != 9:
            settings[k] = widgets[i]["bg"]
        else:
            settings[k] = widgets[i]["text"]
        i += 1
    with open(SETTINGS_JSON, 'w') as outfile:
        json.dump(settings, outfile)
    messagebox.showinfo(title="Settings file written", message="Settings file has been sucessfully written")
    load_graphics_settings()

def select_image(widget):
    valid_files = [
        ("PNG", "*.png"),
        ("JPG", "*.jpg"),
        ("JPEG", "*.jpeg"),
        ("PGM", "*.pgm"),
        ("PPM", "*.ppm"),
        ("BMP", "*.bmp")
    ]
    file = tkinter.filedialog.askopenfile(initialdir="./",filetypes=valid_files)
    if file != None:
        image = Image.open(file.name)
        image = image.resize((40, 40))
        king = ImageTk.PhotoImage(image)
        widget.config(image=king, text=file.name)
        widget.photo = king

def reset_options(root, opt):
    try:
        os.remove(SETTINGS_JSON)
    except:
        pass
    messagebox.showinfo(title="Settings file reset", message="Settings file has been successfully reset")
    root.destroy()
    root.__init__()
    main(root)

def main(root):
    load_graphics_settings()
    root.title("Checkers Settings")
    try:
        with open(SETTINGS_JSON, 'r') as settings:
            options = json.load(settings)
    except:
        options = {
            "bwhite": rgb_to_html((227, 182, 84)),
            "bblack": rgb_to_html((179, 142, 64)),
            "p1bg": rgb_to_html((235, 106, 106)),
            "p1fg": rgb_to_html((186, 63, 52)),
            "p1king": rgb_to_html((140, 14, 0)),
            "p1image": "./resources/king.png",
            "p2bg": rgb_to_html((61, 60, 56)),
            "p2fg": rgb_to_html((43, 42, 40)),
            "p2king": rgb_to_html((0, 0, 0)),
            "p2image": "./resources/king.png",
            "turn": rgb_to_html((255, 255, 0))
        }

    fontstyle = tkinter.font.Font(family="Lucida Grande", size=15)
    title = tkinter.Label(text="Checker Settings", font=fontstyle)
    title.grid(row=1, column=2, pady=5)

    labels = ["Board (WHITE)", "Board (BLACK)", 
              "P1 (BG)", "P1 (FG)", "P1 (KING)", "P1 (KING)", 
              "P2 (BG)", "P2 (FG)", "P2 (KING)", "P2 (KING)", 
              "TURN"]

    while True:
        try:
            modifiers = []
            padding = (120, 0)
            i = 0
            for k, v in options.items():
                label = tkinter.Label(root, text=labels[i])

                if i != 5 and i != 9:
                    modifier = tkinter.Button(root, text="    ", bg=v)
                    modifier["command"] = lambda arg=modifier: choose_color(arg)
                else:
                    image = Image.open(v)
                    image = image.resize((40, 40))
                    king = ImageTk.PhotoImage(image)
                    modifier = tkinter.Button(image=king, text=v)
                    modifier["command"] = lambda arg=modifier: select_image(arg)
                    modifier.photo = king

                modifiers.append(modifier)
                label.grid(row=i+2, column=1, padx=padding)
                modifier.grid(row=i+2, column=2, pady=5)
                i += 1
            break
        except:
            os.remove(SETTINGS_JSON)
            options = {
                "bwhite": rgb_to_html((227, 182, 84)),
                "bblack": rgb_to_html((179, 142, 64)),
                "p1bg": rgb_to_html((235, 106, 106)),
                "p1fg": rgb_to_html((186, 63, 52)),
                "p1king": rgb_to_html((140, 14, 0)),
                "p1image": "./resources/king.png",
                "p2bg": rgb_to_html((61, 60, 56)),
                "p2fg": rgb_to_html((43, 42, 40)),
                "p2king": rgb_to_html((0, 0, 0)),
                "p2image": "./resources/king.png",
                "turn": rgb_to_html((255, 255, 0))
            }
            
    create_button = tkinter.Button(root, text="Write settings file", command=lambda a=modifiers, b=options.keys(): create_settings(a, b))
    create_button.grid(row=i+2, column=2)
    reset_button = tkinter.Button(root, text="Reset to default", command=lambda a=root, b=options: reset_options(a, b), bg="#FF3333")
    reset_button.grid(row=i+3, column=1)

    root.geometry("500x550")
    root.mainloop()

if __name__ == "__main__":
    root = tkinter.Tk()
    main(root)
