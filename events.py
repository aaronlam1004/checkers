import os
import time
import pygame

RESOURCE_PATH = os.path.join(os.path.dirname(__file__), "resources")

pygame.mixer.init()
move_sound = pygame.mixer.Sound(os.path.join(RESOURCE_PATH, "audio/piece-move.wav"))

def mouse_board_coords(window, border, n, pos_m):
    width, height = window.get_rect().size
    metric_x = (width - border) // n
    metric_y = (height - border) // n
    return (pos_m[1] // metric_y, pos_m[0] // metric_x)

def is_in_button_area(area):
    x, y = pygame.mouse.get_pos()
    return x >= area[0] and x <= area[1] and y >= area[2] and y <= area[3]

def get_selected_piece(window, board, border, n, valid):
    mouse_pos = pygame.mouse.get_pos()
    bcoords = mouse_board_coords(window, border, n, mouse_pos)
    piece = board.get_piece(bcoords)
    if piece != None and piece in valid:
        return piece, board.get_piece_moves(piece), bcoords
    return None, [[], []], bcoords

def move_piece(board, piece, moves, bcoords):
    global move_sound
    sound = move_sound
    captures = moves[1]
    for i in range(len(moves[0])):
        move = moves[0][i]
        if move[0] == bcoords[0] and move[1] == bcoords[1]:
            moved = True
            capture = None 
            if len(captures) > 0:
                capture = captures[i]
            next_moves = board.make_move(piece, move, capture)
            sound.play()
            if len(next_moves[1]) == 0:
                board.change_turn()
                return None, [[], []], capture, 1
            else:
                return piece, next_moves, capture, 1
    return None, [[], []], None, 0
