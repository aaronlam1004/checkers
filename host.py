import socket
from game import *
import random
from _thread import *

def read_thread(cli):
    global game
    global player
    while True:
        data = cli.recv(1024)
        if data:
            d = data.decode("utf-8").split('\n')
            if int(d[0]) == player:
                pcoords = d[1].split(' ')
                pcoords = (int(pcoords[0]), int(pcoords[1]))
                piece = game.board.get_piece(game.board.reflect_move(pcoords))

                coords = d[2].split(' ')
                coords = (int(coords[0]), int(coords[1]))

                game.board.make_move(piece, game.board.reflect_move(coords), None)
                game.board.change_turn()

HOST = "127.0.0.1"
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

print(f"Running server at {HOST}:{PORT}")
s.bind((HOST, PORT))


while True:
    s.listen()
    cli, addr = s.accept()
    print("Connected by", addr)

    start_new_thread(read_thread, (cli, ))

    player = 0
    game = Game(name=f"checkers (player {player+1})")
    game.play_online(0, cli)

    break

    # while running:
    #     data = conn.recv(1024)
    #     if not data:
    #         break
    #     print(repr(data))
    #     print(board)
    #     cli.sendall(data)
