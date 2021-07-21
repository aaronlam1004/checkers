import socket
from game import *
from host import read_thread
from _thread import *

def read_thread(cli):
    global game
    global player
    while True:
        data = cli.recv(1024)
        if data:
            d = data.decode("utf-8").split('\n')
            # print(d)
            pcoords = d[1].split(' ')
            pcoords = (int(pcoords[0]), int(pcoords[1]))
            piece = game.board.get_piece(game.board.reflect_move(pcoords))

            coords = d[2].split(' ')
            coords = (int(coords[0]), int(coords[1]))

            capture = None
            if len(d) == 4:
                ccoords = d[3].split(' ')
                ccoords = (int(ccoords[0]), int(ccoords[1]))
                rccoords = game.board.reflect_move(ccoords)
                capture = game.board.board[rccoords[0]][rccoords[1]]

            game.board.make_move(piece, game.board.reflect_move(coords), capture)

            if int(d[0]) == player:
                game.board.change_turn()

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 5000

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
