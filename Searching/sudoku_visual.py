""" 
The Sudoku Backtracking Visaliser for main.py (Algrow)
"""


import pygame as pg
from typing import List, Tuple

from visual_helpers import *

# Colors 
SAFE = HIGHLIGHT1
SELECT = HIGHLIGHT2


def get_grid() -> List[List[int]]:
    """ Retuns the Grid that the SudokuBoard
    is based off of """
    return [
    [0, 1, 6, 5, 0, 8, 4, 0, 2],
    [5, 2, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 7, 6, 0, 0, 0, 3, 1],
    [0, 6, 3, 0, 1, 0, 0, 8, 0],
    [9, 0, 4, 8, 6, 3, 0, 0, 5],
    [0, 5, 0, 0, 0, 0, 6, 0, 0],
    [1, 0, 0, 9, 0, 0, 2, 0, 0],
    [6, 0, 2, 3, 0, 0, 8, 0, 4],
    [0, 4, 5, 0, 0, 0, 0, 1, 0]
    ]
    
    
# The global Grid
grid = get_grid()


class SudokuTile:
    """ 
    A SudokuTile that keeps track of information we need for the
    GUI 
    
    ==== Public Attributes ====
    rect: The coordinates of this Tile
    val: The value/number of this Tile
    known: Whether we knew the value of this Tile
            beforehand or not
    selected: Whether this tile is the one we're guessing
    guess: The gueesing value for this tile
    """
    
    rect: Tuple[int]
    val: int
    known: bool
    selected: bool
    guess: int

    def __init__(self, rect, val=0):
        """ Initializes a SudokuTile object """
        self.rect = rect
        self.val = val
        self.guess = 0
        if val != 0:
            self.known = True
        else:
            self.known = False
        self.selected = False
        
        
    def draw(self, screen: pg.Surface) -> None:
        """ Draws the <SudokuTile> on <screen> """
        
        # If guessing highlight and show orange outline
        if not self.known and self.selected and (self.val != 0 or self.guess != 0):
            pg.draw.rect(screen, LIGHT_BG, self.rect)
            self._draw_border(screen, SELECT)
            
        # if guess is right, show Green outline
        elif not self.known and self.val != 0:
            self._draw_border(screen, SAFE)
        
        pg.draw.rect(screen, TEXT, self.rect, 1)
        
        pos = self.rect[0] + (20), self.rect[1] + 2
        if self.val != 0 and self.known:
            write_text(screen, str(self.val), get_font(60), TEXT, pos)
        elif self.val != 0 and not self.known:
            write_text(screen, str(self.val), get_font(60), HIGHLIGHT1, pos)
        elif self.guess != 0 and self.selected:
            write_text(screen, str(self.guess), get_font(60), HIGHLIGHT2, pos)        
            
    
    def _draw_border(self, screen: pg.Surface, color: Tuple[int], thick=2) -> None:
        """ Draws a border around the tile on <screen> """
        diff = thick // 2 + (2)
        rect = (self.rect[0] + diff + 1, self.rect[1] + diff,
                self.rect[2] - thick - 6, self.rect[3] - thick - 6)
        pg.draw.rect(screen, color, rect, thick)
        
        
    def finish(self, screen) -> None:
        """ Draw the tile when <SudokuBoard> is 
        complete """
        pos = self.rect[0] + (20), self.rect[1] + 2
        pg.draw.rect(screen, TEXT, self.rect, 1)
        write_text(screen, str(self.val), get_font(60), TEXT, pos)
   
    
class SudokuBoard:
    
    """ 
    A SudokuBoard which we solve using backtracking.
    It keeps track of all it's tiles in a 2-D List
    
    ==== Public Attributes ====
    tiles: All the SudokuTiles in the SudokuBoard
    """
    
    tiles: List[List[SudokuTile]]
    
    def __init__(self):
        """ Initalizes a SudokuBoard object """     
        self.tiles = []
        # grid = get_grid()
        delta_x = (WIDTH - 10) // 9
        delta_y = (HEIGHT - 6.5) // 9
        
        x, y = 5, 7
        for row in range(9):
            rows = []
            for col in range(9):
                coords = (x + (col * delta_x), y + (row * delta_y), delta_x, delta_y)
                rows.append(SudokuTile(coords, grid[row][col]))
            self.tiles.append(rows)


    def draw(self, screen) -> None:
        """ Draws the SudokuBoard on <screen> """
        clear_screen(screen)
        self._fill_edges(screen)
        for row in self.tiles:
            for tile in row:
                tile.draw(screen)
                
        
        pg.display.flip()
                
                
    def _fill_edges(self, screen) -> None:
        """ Fills the edges of screen with the Right color, 
        for a better display """
        pg.draw.rect(screen, TEXT, (0, 0, WIDTH, 7))
        pg.draw.rect(screen, TEXT, (0, 0, 5, HEIGHT))
        pg.draw.rect(screen, TEXT, (WIDTH - 5, 0, 5, HEIGHT))
        pg.draw.rect(screen, TEXT, (0, HEIGHT - 8, WIDTH, 8))
        
        pg.draw.rect(screen, TEXT, (212, 0, 6, HEIGHT))
        pg.draw.rect(screen, TEXT, (422, 0, 6, HEIGHT))
        
        pg.draw.rect(screen, TEXT, (0, 199, WIDTH, 6))
        pg.draw.rect(screen, TEXT, (0, 394, WIDTH, 6))
        
                
                
    def get_tile(self, row: int, col: int) -> SudokuTile:
        """ Get the SudokuTile at <row> <col> in the board """
        if 0 <= row <= 8 and 0 <= col <= 8:
            return self.tiles[row][col]
        
        
    def set_tile(self, row: int, col: int, val: int) -> None:
        """ Set the value of SudokuTile at <row> <col> """
        if 0 <= row <= 8 and 0<= col <= 8:
            self.tiles[row][col].val = val
            
            
    def is_safe(self,row: int, col: int, val: int) -> bool:
        """ Return whether the tile at <row> <col> is safe 
        according to Sudoku Rules"""

        # check rows and columns
        rows = [tile.val for tile in self.tiles[row]]
        cols = [self.tiles[i][col].val for i in range(9)]
        if val in cols or val in rows:
            return False
        
        # check box
        row, col = row - (row % 3), col - (col % 3)
        for i in range(3):
            for k in range(3):
                if self.get_tile(row + i, col + k).val == val:
                    return False
        return True
    
    
    def select(self, row: int, col: int) -> None:
        """ Select a Tile - mainly used for displaying the
        tile where the guessing is happening"""
        for rows in self.tiles:
            for tile in rows:
                tile.selected = False
        
        select = self.get_tile(row, col)
        select.selected = True
        
        
    def find_empty(self) -> List[int]:  
        """ Return the first value that is not known 
        on the SudokuBoard, return [-1, -1] otherwise"""
        loc = [-1, -1]
        for i, row in enumerate(self.tiles):
            for k, tile in enumerate(row):
                if tile.val == 0:
                    loc = [i, k]
                    return loc
        return loc
    
    
    def guess(self, row: int, col: int, val: int) -> None:
        """ Assigns the val to the <SudokuTile> guess attribute """
        tile = self.get_tile(row, col)
        tile.guess = val
                    
        
    def solve(self, screen) -> bool: 
        """ Solve the SudokuBoard using the BackTracking
        Algorithm """        
        row, col = self.find_empty()
        
        if row == -1 or col == -1:
            return True
        
        for guess in range(1, 10):
            
            self.select(row, col)
            self.guess(row, col, guess)
            self.draw(screen)

            # So the user can leave midway
            for e in pg.event.get():            
                if e.type == pg.QUIT:
                    pg.quit()
                    exit()
            
            if self.is_safe(row, col, guess):
                self.set_tile(row, col, guess)
                self.draw(screen)
                
                if self.solve(screen):
                    return True
                
                self.set_tile(row, col, 0)
                self.draw(screen)
                
            pg.time.delay(50)
            pg.display.flip()
                  
        return False


    def finished(self, screen) -> None:
        """ Draws the screen when the SudokuBoard
        is solved """
        clear_screen(screen)
        for rows in self.tiles:
            for tile in rows:
                tile.finish(screen)
                
        self._fill_edges(screen)
        pg.display.flip()
        
        
if __name__ == '__main__':
    pass
                