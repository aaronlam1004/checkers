import os
import sys
import socket
import random
import threading
import signal
import select
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from checkers import Checkers

game = None
stop = False
s = None

def stop_game():
    global game
    if game != None:
        print("Stopping game")
        game.running = False
        game = None

def stop_socket():
    global s
    global stop
    if s != None:
        stop = True
        s = None

def valid_ip(ip):
    def isIPv4(s):
        try: 
            return 0 <= int(s) <= 255
        except:
            return False

    if ip.count('.') == 3 and all(isIPv4(i) for i in ip.split('.')):
        return True

    return False

def read_thread(cli, uid, game):
    while True:
        try:
            data, _, _ = select.select([cli], [], [])
            if data:
                data = cli.recv(1024)
                d = data.decode("utf-8")
                if d == "ready":
                    game.opp_ready = True
                elif d == "goodbye":
                    print("Killing player", uid, "thread")
                    game.running = False
                    break
                else:
                    d = d.split('\n')
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

                    if int(d[0]) == uid:
                        game.board.change_turn()
        except:
            print("Killing player", uid, "thread")
            break

def host_server(ip, port):
    global game
    global s
    global stop

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print(f"Running server at {ip}:{port}")
    s.bind((ip, port))
    s.setblocking(True)
    s.settimeout(1.0)
    while True:
        try:
            s.listen()
            cli, addr = s.accept()
            print(f"Connection established by {addr[0]}:{addr[1]}")

            player = 0
            print("Starting player", player, "thread")

            game = Checkers(name=f"Checkers (player {player+1})")
            t = threading.Thread(target=read_thread, args=(cli, player, game, ))
            t.start()
            
            game.play_online(0, cli)
            break
        except socket.timeout:
            if stop:
                stop = False
                break
            else:
                continue
        except:
            break

    game = None
    s = None

def connect_to_server(ip, port):
    global game

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Connecting to server at {ip}:{port}")
    s.connect((ip, port))

    player = 1
    print("Starting player", player, "thread")

    game = Checkers(name=f"Checkers (player {player+1})", reflect=True)
    t = threading.Thread(target=read_thread, args=(s, player, game, ))
    t.start()

    game.play_online(1, s)
    game = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Host or join a checkers game.")

    parser.add_argument("connectype", choices=["host", "join"], default=None, help="determines whether to host or join a game")
    parser.add_argument("--ip", help="IP address to host/connect")
    parser.add_argument("--port", type=int, help="port to host/connect")
    
    args = parser.parse_args()

    HOST = "127.0.0.1"
    PORT = 5000

    blocked_ports = [80, 22, 25, 465, 587]

    if args.connectype == "host":
        if args.ip != None and valid_ip(args.ip):
            HOST = args.ip

        if args.port != None and args.port not in blocked_ports:
            PORT = args.port

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        print(f"Running server at {HOST}:{PORT}")
        s.bind((HOST, PORT))


        while True:
            s.listen()
            cli, addr = s.accept()
            print(f"Connection established by {addr[0]}:{addr[1]}")

            player = 0
            game = Checkers(name=f"Checkers (player {player+1})")
            
            t = threading.Thread(target=read_thread, args=(cli, player, game, ))
            print("Starting player", player, "thread")
            t.start()
            
            game.play_online(0, cli)
            break
            
    elif args.connectype == "join":
        if args.ip != None and valid_ip(args.ip):
            HOST = args.ip
            
        if args.port != None and args.port not in blocked_ports:
            PORT = args.port

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting to server at {HOST}:{PORT}")
        s.connect((HOST, PORT))

        player = 1
        game = Checkers(name=f"Checkers (player {player+1})", reflect=True)
        
        t = threading.Thread(target=read_thread, args=(s, player, game ))
        print("Starting player", player, "thread")
        t.start()

        game.play_online(1, s)
        
