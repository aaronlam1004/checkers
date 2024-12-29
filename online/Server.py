import sys
import os
import socket
import select
import json
from threading import Thread
from enum import IntEnum

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from board.StandardBoard import StandardBoard
from scene.GameScene import GameScene
from scene.SceneHandler import SceneHandler, SceneSignals
from ui.Window import Window

class OnlineState(IntEnum):
    IDLE = 0
    PLAYING = 1

class Server:
    sock = None
    game_scene = None
    running = False
    state = OnlineState.IDLE
    
    @staticmethod
    def start():
        print("Starting server")
        Server.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Server.sock.bind(("localhost", 1234))
        Server.sock.setblocking(True)
        Server.sock.settimeout(1.0)
        Server.state = OnlineState.IDLE

    @staticmethod
    def read(client):
        while Server.running:
            data, _, _ = select.select([client], [], [])
            if data:
                timeouts = 0
                data = client.recv(1024)
                print(data)
                client.sendall(data)

    @staticmethod
    def run():
        Server.timeouts = 0
        Server.running = True
        while Server.running:
            try:
                Server.sock.listen()
                client, addr = Server.sock.accept()
                print("Connection established")
                Server.game_scene.board_ui.set_socket(client)
                Server.game_scene.board_ui.set_player_id(0)
                Server.read(client)
            except socket.timeout:
                pass

    @staticmethod
    def stop():
        Server.running = False

    @staticmethod
    def set_game_scene(game_scene: GameScene):
        Server.game_scene = game_scene

window = Window((800, 700), "Checkers")
board = StandardBoard()
board.setup()
board.enable_blitz_mode()
game_scene = GameScene(window.screen, board, is_online=True)

SceneHandler.set_scene(game_scene)

Server.start()
server_thread = Thread(target=Server.run)
Server.set_game_scene(game_scene)
server_thread.start()

while True:
    signal_id, data = SceneHandler.handle_events()
    if signal_id == SceneSignals.QUIT:
        Server.stop()
        break
    game_scene.update()
    window.update()
server_thread.join()
