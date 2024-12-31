from typing import Tuple, Optional

import pygame
from pygame.surface import Surface

from Resources import Images
from Settings import ColorSettings

def draw_background(screen: Surface) -> None:
    background = pygame.image.load(Images.BACKGROUND.value)
    width, height = background.get_size()
    width *= 2
    height *= 2
    background = pygame.transform.scale(background, (width, height))
    screen.blit(background, (0, 0, width, height))

def draw_text_border(screen: Surface, text_surface: Surface, x: float, y: float, border_size: float) -> None:
    screen.blit(text_surface, (x - border_size, y))
    screen.blit(text_surface, (x - border_size, y - border_size))
    screen.blit(text_surface, (x - border_size, y + border_size))
    screen.blit(text_surface, (x + border_size, y))
    screen.blit(text_surface, (x + border_size, y - border_size))
    screen.blit(text_surface, (x + border_size, y + border_size))
    screen.blit(text_surface, (x, y - border_size))
    screen.blit(text_surface, (x, y + border_size))

def draw_piece(screen: Surface, position: Tuple[float, float], dimension: Tuple[float, float],
               color: Tuple[int, int, int], outline_color: Optional[Tuple[float, float, float]] = None,
               bg_size: int = 20, outline_size: int = 15, is_king: bool = False) -> None:
    x, y = position
    piece_width, piece_height = dimension
    if outline_color:
        pygame.draw.ellipse(screen, outline_color, (x, y, piece_width, piece_height))
        x += (outline_size / 2)
        y += (outline_size / 2)
        piece_width -= outline_size
        piece_height -= outline_size
    color_bg = ColorSettings.get_bg_color(color)
    pygame.draw.ellipse(screen, color_bg, (x, y, piece_width, piece_height))
    x += (bg_size / 2)
    y += (bg_size / 2)
    piece_width -= bg_size
    piece_height -= bg_size
    pygame.draw.ellipse(screen, color, (x, y, piece_width, piece_height))
    if is_king:
        king_img = get_king_img((piece_width / 1.1, piece_height / 1.1), ColorSettings.get_bg_color(color))
        king_width, king_height = king_img.get_size()
        king_rect = (x + 1.1, y + 1.1, king_width, king_height)
        screen.blit(king_img, king_rect)

def get_king_img(dimensions: Tuple[float, float], color: Tuple[int, int, int]) -> Surface:
    king_img = pygame.image.load(Images.KING.value).convert_alpha()
    king_img = pygame.transform.scale(king_img, dimensions)
    king_width, king_height = king_img.get_size()
    r, g, b = color
    for row in range(king_width):
        for col in range(king_height):
            _, _, _, alpha = king_img.get_at((row, col))
            king_img.set_at((row, col), pygame.Color(r, g, b, alpha))
    return king_img
   
