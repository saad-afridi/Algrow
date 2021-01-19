"""
Dimensions, Fonts, Colours, visual helper functions,
random helper functions for Algrow.

Note: Most of the visual helpers require you to flip after using them
"""

import pygame as pg
from typing import Dict, List, Optional, Tuple

# Screen Dimensions
HEIGHT, WIDTH = 600, 640
FONT_HEIGHT = 40
VISUALIZE_HEIGHT = HEIGHT - FONT_HEIGHT - 50 # 600 - 40 - 50 = 510

# Text Styling and Colors
FONT_FAMILY = "inkfree"

# Custom colors
BACKGROUND = (40, 40, 40) # Light
# BARS = (128, 121, 159) # Light bars
TEXT = (180, 180, 180) # Dark


# Anna orig
# BACKGROUND = (105, 0, 191)
BARS = (165, 92, 255)
# TEXT = (231, 177, 250)


# Other Colors
HIGHLIGHT1 = (125, 255, 186) # Light Green
HIGHLIGHT2 = (52, 219, 235) # Dark Neon Blue
LIGHT_BG = (BACKGROUND[0] + 30, BACKGROUND[1] + 30, BACKGROUND[2] + 30)


class PButton():
    
    coord: Tuple[int]
    color: Tuple[int]
    text: Optional[str]
    
    def __init__(self, screen: pg.Surface, coord: Tuple[int], 
                 color = TEXT) -> None:
        self.coord = coord
        self.color = color
        self.screen = screen
        self.text = ""
        self.draw()
        
        
        
    def draw(self) -> None:
        # [WHITE] Outline
        out = (self.coord[0] - 3, self.coord[1] - 3, self.coord[2] + 6, 
               self.coord[3] + 6)
        light_bg = (BACKGROUND[0] + 30, BACKGROUND[1] + 30, BACKGROUND[2] + 30)
        pg.draw.rect(self.screen, light_bg, out)
        
        # Actual button
        pg.draw.rect(self.screen, self.color, self.coord)
        self.add_text(self.text)
        
    
    
    def is_cursor_on(self, pos: Tuple[int], clicked=False) -> bool:
        """Return whether <x> and <y> are within the PButton"""
        
        ans = self.coord[0] < pos[0] < self.coord[0] + self.coord[2] and \
            self.coord[1] < pos[1] < self.coord[1] + self.coord[3]
        
        if not clicked:
            self.hover()
        return ans
        
    
    def hover(self) -> None:
        """Render the drawing action of PButton"""
        
        new_color = (self.color[0] - 60, self.color[1] - 60, self.color[2] - 60)
        pg.draw.rect(self.screen, new_color, self.coord)
        self.add_text(self.text)
        
        
    def add_text(self, text: str) -> None:
        """Add text to current button"""
        
        self.text = text
        pos = (self.coord[0] + (self.coord[2] // 2) - len(text) * 9
               , self.coord[1] + (self.coord[3] // 2) - (FONT_HEIGHT// 2))
        write_text(self.screen, text, get_font(), BACKGROUND, pos)


def draw_header(screen: pg.Surface, text: str, offset=48, thick=5) -> None:
    """Draws the header at the top"""
    
    write_text(screen, text, get_font(), TEXT, 
               (offset, 23))
    pg.draw.rect(screen, TEXT, (offset, 70, WIDTH - (offset * 2), thick))
    
    
def get_font(size=FONT_HEIGHT, bold=False) -> pg.font:
    """Return font of <size>"""
    
    font = pg.font.Font("fonts\Inter-VariableFont_slnt,wght.ttf",
                            size - 8)
    if bold:
        font.set_bold(True)
    return font


def border(screen: pg.Surface, color=TEXT, thick=3) -> None:
    """Draws a Border around the screen"""
    
    pg.draw.rect(screen, color, (5, 5, thick, HEIGHT - 10))
    pg.draw.rect(screen, color, (5, 5, WIDTH - 10, thick))
    pg.draw.rect(screen, color, (WIDTH - thick - 5, 5, thick, HEIGHT - 10))
    pg.draw.rect(screen, color, (5, HEIGHT - thick - 5, WIDTH - 10, thick))


def title_screen(screen: pg.Surface) -> None:
    """Draws the title screen of the program"""
    
    font = pg.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)

    clear_screen(screen)
    border(screen)

    write_text(screen, "Algrow", get_font(72), TEXT, (210, 210))
    pg.draw.rect(screen, TEXT, (50, 310, 540, 10))

    time_loop(screen, 3000)


def two_options(screen: pg.Surface) -> None:
    """Draws two rectangles plus a title at the top"""
    
    pg.draw.rect(screen, TEXT, (40, 225, 560, 150))
    pg.draw.rect(screen, TEXT, (40, 410, 560, 150))


def three_options(screen: pg.Surface) -> None:
    """Draws three rectangles evenly divided"""
    
    pg.draw.rect(screen, TEXT, (40, 40, 560, 150))
    pg.draw.rect(screen, TEXT, (40, 225, 560, 150))
    pg.draw.rect(screen, TEXT, (40, 410, 560, 150))


def write_text(screen: pg.Surface, text: str, font: pg.font, color: Tuple,
               pos: Tuple) -> None:
    """Write the <text> on <screen> at <post> with <font> and <color>"""
    
    text_surface = font.render(text, 1, color)
    screen.blit(text_surface, pos)
    

def clear_screen(screen: pg.Surface, color=BACKGROUND) -> None:
    """Clears screen i.e. draws a rectangle that
    covers the whole <screen> of color <BACKGROUND>"""
    
    pg.draw.rect(screen, color, (0, 0, WIDTH, HEIGHT))
    

def time_loop(screen: pg.Surface, timer: int) -> None:
    """Makes the current display on screen stay for <timer> 
    (milliseconds) long""" 
    
    clock = pg.time.Clock()
    time_elapsed = 0
    while time_elapsed < timer:
        
        dt = clock.tick()
        time_elapsed += dt
        
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit()
        pg.display.flip()
        
if __name__ == '__main__':
    pass