import pygame

def paint_king(king, color):
    width, height = king.get_size()
    r, g, b = color
    for x in range(width):
        for y in range(height):
            alpha = king.get_at((x, y))[3]
            king.set_at((x, y), pygame.Color(r, g, b, alpha))

def draw_king(window, x, y, metric_x, metric_y, player):
    img = pygame.image.load("./resources/king.png").convert_alpha()
    img = pygame.transform.scale(img, (metric_x - 14, metric_y - 14))
    if player == 0:
        paint_king(img, (140, 14, 0))
    else:
        paint_king(img, (0, 0, 0))
    img_rect = (x + 6, y + 4, metric_x - 14, metric_y - 14)
    window.blit(img, img_rect) 

def draw_board(window, board, resol, border, n, highlighted, captor, show=True):
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
                pygame.draw.rect(window, (227, 182, 84), (x, y, metric_x, metric_y))
            else:
                pygame.draw.rect(window, (179, 142, 64), (x, y, metric_x, metric_y))
            x += metric_x
        x = border / 2
        y += metric_y

    for piece in board.pieces['0'][:board.end['0']]:
        x = (piece.col * metric_x) + (border / 2)
        y = (piece.row * metric_y) + (border / 2)
        if board.turn == 0 and piece in valid_pieces:
            pygame.draw.ellipse(window, (0, 0, 255), (x, y, metric_x, metric_y))
            pygame.draw.ellipse(window, (235, 106, 106), (x + 3, y + 3, metric_x - 6, metric_y - 6))
            pygame.draw.ellipse(window, (186, 63, 52), (x + 8, y + 8, metric_x - 16, metric_y - 16))
        else:
            pygame.draw.ellipse(window, (235, 106, 106), (x, y, metric_x, metric_y))
            pygame.draw.ellipse(window, (186, 63, 52), (x + 5, y + 5, metric_x - 10, metric_y - 10))
        if piece.isking:
            draw_king(window, x, y, metric_x, metric_y, 0)

    for piece in board.pieces['1'][:board.end['1']]:
        x = (piece.col * metric_x) + (border / 2)
        y = (piece.row * metric_y) + (border / 2)
        if board.turn == 1 and piece in valid_pieces:
            pygame.draw.ellipse(window, (0, 0, 255), (x, y, metric_x, metric_y))
            pygame.draw.ellipse(window, (61, 60, 56), (x + 3, y + 3, metric_x - 6, metric_y - 6))
            pygame.draw.ellipse(window, (43, 42, 40), (x + 8, y + 8, metric_x - 16, metric_y - 16))
        else:
            pygame.draw.ellipse(window, (61, 60, 56), (x, y, metric_x, metric_y))
            pygame.draw.ellipse(window, (43, 42, 40), (x + 5, y + 5, metric_x - 10, metric_y - 10))
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
