"""
Dimensions, Fonts, Colours, visual helper functions,
random helper functions for Algrow.

Note: Most of the visual helpers require you to flip after using them
"""

import pygame as pg
from typing import Tuple

# Screen Dimensions
HEIGHT, WIDTH = 600, 640
FONT_HEIGHT = 40
VISUALIZE_HEIGHT = HEIGHT - FONT_HEIGHT - 50

# Text Styling and Colors
FONT_FAMILY = "Consolas"
# BACKGROUND = (105, 0, 191)
# BARS = (165, 92, 255)
# TEXT = (231, 177, 250)

# Custom colors
BORDER = (0, 0, 0)
# (18, 9, 97)
# BACKGROUND = (67, 59, 103)
BACKGROUND = (0, 0, 0)
BARS = (148, 141, 179)
TEXT = (149, 61, 255)
# 149, 61, 255


# HIGHLIGHT: (75, 10, 99)

# Anna orig
# BACKGROUND = (105, 0, 191)
# BARS = (165, 92, 255)
# TEXT = (231, 177, 250)


# STD_FONT = pg.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)

def border(screen: pg.Surface, color=TEXT, thick=3) -> None:
    """ Draws a Border around the screen """
    pg.draw.rect(screen, color, (5, 5, thick, HEIGHT - 10))
    pg.draw.rect(screen, color, (5, 5, WIDTH - 10, thick))
    pg.draw.rect(screen, color, (WIDTH - thick - 5, 5, thick, HEIGHT - 10))
    pg.draw.rect(screen, color, (5, HEIGHT - thick - 5, WIDTH - 10, thick))


def write_text(screen: pg.Surface, text: str, font: pg.font, color: Tuple,
               pos: Tuple) -> None:
    """
    Write the <text> on <screen> at <post> with <font> and <color>
    """
    text_surface = font.render(text, 1, color)
    screen.blit(text_surface, pos)


def title_screen(screen: pg.Surface) -> None:
    """
    Draws the title screen of the program
    """
    font = pg.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)

    clear_screen(screen)
    border(screen)
    pg.draw.rect(screen, BARS, (0, 0, WIDTH, HEIGHT))
    write_text(screen, "Algrow", font, BACKGROUND, (270, 255))
    pg.draw.rect(screen, BACKGROUND, (50, 310, 540, 10))

    clock = pg.time.Clock()
    time_elapsed = 0
    while True:
        dt = clock.tick()
        time_elapsed += dt

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        if time_elapsed > 3000:
            return

        pg.display.flip()


def two_options(screen: pg.Surface) -> None:
    """
    Draws two rectangles plus a title at the top
    """
    pg.draw.rect(screen, TEXT, (40, 225, 560, 150))
    pg.draw.rect(screen, TEXT, (40, 410, 560, 150))


def three_options(screen: pg.Surface) -> None:
    """
    Draws three rectangles evenly divided
    """
    pg.draw.rect(screen, TEXT, (40, 40, 560, 150))
    pg.draw.rect(screen, TEXT, (40, 225, 560, 150))
    pg.draw.rect(screen, TEXT, (40, 410, 560, 150))


def clear_screen(screen: pg.Surface) -> None:
    """
    Clears screen i.e. draws a rectangle that
    covers the whole <screen> of color <BACKGROUND>
    """
    pg.draw.rect(screen, BACKGROUND, (0, 0, WIDTH, HEIGHT))
