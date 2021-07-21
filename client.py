import socket
from game import *
from _thread import *

HOST = "127.0.0.1"
PORT = 5000

def read_thread(cli):
    global game
    global player
    while True:
        data = s.recv(1024)
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


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

start_new_thread(read_thread, (s, ))

player = 1
game = Game(name=f"checkers (player {player+1})", reflect=True)
game.play_online(1, s)

# while running:
#     if board.gamestate() != -1:
#         break
#     print(board)
#     text = input()
#     s.sendall(bytes(text, "utf-8"))
#     data = s.recv(1024)
