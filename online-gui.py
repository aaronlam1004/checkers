import threading
import os, sys, signal
import tkinter
import tkinter.font

from online import *

exited = False
t = None

def game_thread(name, ip, port):
    global t
    global exited
    print(f"Running GUI {name} thread")
    try:
        if name == "host":
            host_server(ip, port)
            if not exited:
                buttons[0].config(text="Host", command=lambda: create_game(ent))
        else:
            connect_to_server(ip, port)
            if not exited:
                buttons[0].pack()
        if not exited:
            buttons[1].pack()
            status_label.pack_forget()
            status_label.config(text="", bg=default_color)
            status_label.pack()
        print(f"Ending GUI {name} thread")
        t = None
    except:
        print("Errror")
        if not exited:
            if name == "host":
                buttons[0].config(text="Host", command=lambda: create_game(ent))
            else:
                buttons[0].pack()
            buttons[1].pack()
            status_label.pack_forget()
            status_label.config(text=f"ERROR: unable to {name} game", bg="#fc5c38")
            status_label.pack()
        print(f"Ending GUI {name} thread")
        t = None

def send_kill():
    global exited
    if t is not None:
        stop_game()
        stop_socket()
    print("Destroying window")
    exited = True
    root.destroy()
    
def create_game(entries):
    global t

    ip = entries[0].get()
    port = int(entries[1].get())

    buttons[0].config(text="Cancel", command=stop_socket)
    buttons[1].pack_forget()
    status_label.config(text=f"Hosting at {ip}:{port}", bg="#b1f261")
    root.update()

    print("Game thread to host (in GUI)")

    t = threading.Thread(target=game_thread, args=("host", ip, port, ))
    t.start()

def join_game(entries):
    global t
    ip = entries[0].get()
    port = int(entries[1].get())

    for button in buttons:
        button.pack_forget()

    status_label.config(text=f"Connecting to {ip}:{port}", bg="#b1f261")
    root.update()

    print("Game thread to join (in GUI)")
    t = threading.Thread(target=game_thread, args=("join", ip, port, ))
    t.start()
   
def set_entries(root):
    entries = []
    
    ipl = tkinter.Label(root, text="IP")
    portl = tkinter.Label(root, text="Port")

    entries.append(tkinter.Entry(root))
    entries.append(tkinter.Entry(root))

    entries[0].insert(0, "127.0.0.1")
    entries[1].insert(0, "5000")

    ipl.pack()
    entries[0].pack()
    portl.pack()
    entries[1].pack()

    return entries

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Checkers Online Play")
    fontstyle = tkinter.font.Font(family="Lucida Grande", size=15)
    tkinter.Label(root, text="Checkers Online Play", font=fontstyle).pack()

    ent = set_entries(root)

    buttons = []
    buttons.append(tkinter.Button(root, text="Host", command=lambda: create_game(ent)))
    buttons.append(tkinter.Button(root, text="Join", command=lambda: join_game(ent)))

    for button in buttons:
        button.pack()

    status_label = tkinter.Label(root)
    status_label.pack()
    default_color = status_label["bg"]

    root.geometry("300x300")
    root.protocol("WM_DELETE_WINDOW", send_kill)
    root.mainloop()
