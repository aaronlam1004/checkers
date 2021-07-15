from StandardBoard import StandardBoard
from game import *
import pygame

if __name__ == "__main__":
    N = 8

    board = StandardBoard()
    board.initialize(N)

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Checkers")

    LENGTH = 700
    BORDER = 20

    screen = pygame.display.set_mode((LENGTH, LENGTH), pygame.RESIZABLE)

    running = True
    button_area = ()
    button_high = False

    # modes:
    #   0 -> main menu
    #   1 -> playing the game
    #   2 -> results (who won or lost)
    mode = 1 

    while running:
        if board.gamestate() != -1:
            mode = 2

        # Fill the background
        screen.fill((255, 255, 255))

        # User events
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONUP:
                if mode == 1:
                    game_handler(screen, board, BORDER, N)
                elif mode == 2:
                    if is_in_button_area(button_area):
                        mode = 1
                        board.initialize(8)
            elif event.type == pygame.MOUSEMOTION:
                if mode == 2:
                    button_high = is_in_button_area(button_area)
            elif event.type == pygame.QUIT:
                running = False
        
        if mode == 0:
            width, height = screen.get_rect().size
            fontsize = int(100*height/LENGTH)
            titlefont = pygame.font.SysFont("Comic Sans MS", fontsize)
            textsurface = titlefont.render("Checkers", False, (0, 0, 0))
            screen.blit(textsurface, (0, 0))

            fontsize = int(fontsize / 2)
            bwidth = 200 * (height / LENGTH)
            bheight = 100 * (height / LENGTH)
            x = width / 2 - (bwidth / 2)
            y = height / 2
            buttonfont = pygame.font.SysFont("Comic Sans MS", fontsize)
            create_button(screen, "PLAY", buttonfont, (0, 0, 0), (x, y), (bwidth, bheight), (255, 0, 0))
            # create_button(screen, "QUIT", buttonfont, (0, 0, 0), (x, y + bheight + bheight / 2), (bwidth, bheight), (255, 0, 0))
        elif mode == 1:
            draw_board(screen, board, screen.get_rect().size, BORDER, N)
        else:
            draw_board(screen, board, screen.get_rect().size, BORDER, N)

            width, height = screen.get_rect().size
            fontsize = int(100 * height / LENGTH)
            titlefont = pygame.font.SysFont("Comic Sans MS", fontsize)
            textsurface = titlefont.render(f"Player {board.gamestate() + 1} wins!!", False, (255, 0, 0))
            twidth, _ = textsurface.get_rect().size
            x = width / 2 - (twidth / 2)
            screen.blit(textsurface, (x, BORDER))

            fontsize = int(fontsize / 2)
            bwidth = 400 * (height / LENGTH)
            bheight = 100 * (height / LENGTH)
            x = width / 2 - (bwidth / 2)
            y = height / 2
            buttonfont = pygame.font.SysFont("Comic Sans MS", fontsize)
            if button_high:
                create_button(screen, "PLAY AGAIN", buttonfont, (0, 0, 0), (x, y), (bwidth, bheight), (255, 255, 0))
            else:
                create_button(screen, "PLAY AGAIN", buttonfont, (0, 0, 0), (x, y), (bwidth, bheight), (255, 0, 0))
            button_area = (x, x + bwidth, y, y + bheight)
            

        # Flip the display
        pygame.display.flip()

    # Quit the game
    pygame.quit()
