import pygame
import json

def html_to_rgb(color):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)

    return (r, g, b)

def paint_king(king, color):
    width, height = king.get_size()
    if type(color) == str:
        r, g, b = html_to_rgb(color)
    else:
        r, g, b = color
    for x in range(width):
        for y in range(height):
            _, _, _, alpha = king.get_at((x, y))
            king.set_at((x, y), pygame.Color(r, g, b, alpha))

def draw_king(window, x, y, metric_x, metric_y, player):
    global options

    if player == 0:
        img = pygame.image.load(options["p1image"]).convert_alpha()
        img = pygame.transform.scale(img, (metric_x - 20, metric_y - 20))
        col = options["p1king"]
        if type(col) is tuple:
            paint_king(img, col)
        else:
            paint_king(img, html_to_rgb(col))
    else:
        img = pygame.image.load(options["p2image"]).convert_alpha()
        img = pygame.transform.scale(img, (metric_x - 20, metric_y - 20))
        col = options["p2king"]
        if type(col) is tuple:
            paint_king(img, col)
        else:
            paint_king(img, html_to_rgb(col))
    img_rect = (x + 9, y + 8, metric_x - 20, metric_y - 20)
    window.blit(img, img_rect) 

def draw_board(window, board, resol, border, n, highlighted, captor, show=True):
    global options

    bwhite = options["bwhite"]
    bblack = options["bblack"]

    turn = options["turn"]
    p1bg = options["p1bg"]
    p1fg = options["p1fg"]
    p2bg = options["p2bg"]
    p2fg = options["p2fg"]

    valid_pieces = []
    if show:
        if captor is None:
            valid_pieces, _ = board.get_all_possible_moves()
        else:
            valid_pieces = [captor]

    width = resol[0]
    height = resol[1]

    metric_x = (width - border) // n
    metric_y = (height - border) // n
    x = border / 2
    y = border / 2
    for row in range(board.n):
        for col in range(board.n):
            if (row + col) % 2 == 0:
                pygame.draw.rect(window, bwhite, (x, y, metric_x, metric_y))
            else:
                pygame.draw.rect(window, bblack, (x, y, metric_x, metric_y))
            x += metric_x
        x = border / 2
        y += metric_y

    for piece in board.pieces['0'][:board.end['0']]:
        x = (piece.col * metric_x) + (border / 2)
        y = (piece.row * metric_y) + (border / 2)
        if board.turn == 0 and piece in valid_pieces:
            pygame.draw.ellipse(window, turn, (x, y, metric_x, metric_y))
            pygame.draw.ellipse(window, p1bg, (x + 3, y + 3, metric_x - 6, metric_y - 6))
            pygame.draw.ellipse(window, p1fg, (x + 8, y + 8, metric_x - 16, metric_y - 16))
        else:
            pygame.draw.ellipse(window, p1bg, (x, y, metric_x, metric_y))
            pygame.draw.ellipse(window, p1fg, (x + 5, y + 5, metric_x - 10, metric_y - 10))
        if piece.isking:
            draw_king(window, x, y, metric_x, metric_y, 0)

    for piece in board.pieces['1'][:board.end['1']]:
        x = (piece.col * metric_x) + (border / 2)
        y = (piece.row * metric_y) + (border / 2)
        if board.turn == 1 and piece in valid_pieces:
            pygame.draw.ellipse(window, turn, (x, y, metric_x, metric_y))
            pygame.draw.ellipse(window, p2bg, (x + 3, y + 3, metric_x - 6, metric_y - 6))
            pygame.draw.ellipse(window, p2fg, (x + 8, y + 8, metric_x - 16, metric_y - 16))
        else:
            pygame.draw.ellipse(window, p2bg, (x, y, metric_x, metric_y))
            pygame.draw.ellipse(window, p2fg, (x + 5, y + 5, metric_x - 10, metric_y - 10))
        if piece.isking :
            draw_king(window, x, y, metric_x, metric_y, 1)

    for move in highlighted[0]:
        width, height = window.get_rect().size
        metric_x = (width - border) // n
        metric_y = (height - border) // n
        x = (move[1] * metric_x) + (border / 2)
        y = (move[0] * metric_y) + (border / 2)
        pygame.draw.rect(window, (255, 0, 0), (x, y, metric_x, metric_y))

    return valid_pieces

def draw_button(window, text, font, fontcolor, loc, size, buttoncolor):
    buttontext = font.render(text, False, fontcolor)
    x, y = loc
    width, height = size
    pygame.draw.rect(window, buttoncolor, (x, y, width, height))

    bw, bh = buttontext.get_size()
    w = width - bw
    h = height - bh
    window.blit(buttontext, (x + (w / 2), y + (h / 2)))

try:
    with open("./settings.json") as infile:
        options = json.load(infile)
except:
    options = {
        "bwhite": (227, 182, 84),
        "bblack": (179, 142, 64),
        "p1bg": (235, 106, 106),
        "p1fg": (186, 63, 52),
        "p1king": (140, 14, 0),
        "p1image": "./resources/king.png",
        "p2bg": (61, 60, 56),
        "p2fg": (43, 42, 40),
        "p2king": (0, 0, 0),
        "p2image": "./resources/king.png",
        "turn": (255, 255, 0)
    }
