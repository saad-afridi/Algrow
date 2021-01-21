
""" 
The A* Visualiser for main.py 
"""

import pygame as pg
from typing import List, Tuple, Optional, Dict

from visual_helpers import *


class MazeTile:
    """ 
    A MazeTile on the pygame GUI
    
    ==== Public Attributes ====
    parent: The parent of this MazeTile
    coord: The coordinates of this MazeTile on the pygame window
    pos: The position of this MazeTile on the maze
    val: Indicates whether the MazeTile is an obstacle/or not
    cost: Cost of walking on this MazeTile
    dist: Distance between the end and this MazeTile
    heur: Heuristic of this tile 
    """
    
    parent: object
    coord: Tuple[int]
    pos = Tuple[int]
    val: int
    cost: int 
    dist: int 
    heur: int
    
    
    def __init__(self, coord: Tuple[int], parent=None, pos=None, val=1) -> None:
        """ Initaliez a MazeTile object """
        self.coord = coord
        self.parent = parent
        self.pos = pos
        
        self.val = val
        
        self.cost = 0
        self.dist = 0
        self.heur = 0
        
        
    def is_cursor_on(self, x: int, y: int) -> bool:
        """ Returns whether <x> and <y> are within this tile's
        bounds """
        return self.coord[0] < x < self.coord[0] + self.coord[2] \
            and self.coord[1] < y < self.coord[1] + self.coord[3] 
            
            
    def switch(self, val=0) -> bool:
        """ Change whether the tile is an obstacle or not """
        self.val = val
    
    
    def draw(self, screen: pg.Surface) -> None:
        """ Draws the tile on <screen> """
        if self.cost != 0:
            green = 155 + (self.cost // 7)
            if green > 255:
                green = 255
            blue = 235 - (self.cost // 7)
            if blue < 0:
                blue = 0
            color = (135, green, blue)
            pg.draw.rect(screen, color, self.coord) 
        elif self.val == 1:
            pg.draw.rect(screen, (105, 105, 105), self.coord)
        elif self.val == 0:
            pg.draw.rect(screen, BACKGROUND, self.coord)
    
    
    def __eq__(self, other: object) -> None:
        """ Return whether other is equal to self """
        if isinstance(other, MazeTile):  
            return self.coord == other.coord
        return False
    
    
    def __lt__(self, other: object) -> None:
        """ Return whether self is less than other """
        if isinstance(other, MazeTile):
            return self.cost < other.cost
        return False
    
    
    def __gt__(self, other: object) -> None:
        """ Return whether self is greater than other """
        if isinstance(other, MazeTile):
            return self.cost > other.cost
        return False
            
            
    def __str__(self) -> str:
        """ Return a string represtation of a MazeTile """
        return "[" + str(self.pos) + "|" + str(self.val) + "|" + str(self.cost) + "]" 
        

class Maze:
    """ 
    The Whole Mazy which keeps tracks of all it's tiles
    
    ==== Public Attributes ====
    tiles: All the MazeTile in this Maze
    start: The starting position of the path
    end: The ending position of the path
    selected: The current tile being inspected in the
                algorithm
    """
    
    
    tiles: List[MazeTile]
    start: MazeTile
    end: MazeTile
    selected: MazeTile
    
    
    def __init__(self):
        """ Initalizes a Maze (40x40) """
        x, y = 0, 0
        delta_x, delta_y = WIDTH // 40, HEIGHT // 40
        self.tiles = []
        self.start, self.end = None, None
        self.selected = None
        
        for row in range(40):
            rows = []
            for col in range(40):
                coords = (x + (row * delta_x), y + (col * delta_y),
                          delta_x, delta_y)
                tile = MazeTile(coord= coords, pos=(row, col))
                rows.append(tile)
            self.tiles.append(rows)
            
            
    def draw(self, screen: pg.Surface) -> None:
        """ Draws the Maze """
        clear_screen(screen)
        for row in self.tiles:
            for tile in row:
                if tile == self.start:
                    pg.draw.rect(screen, HIGHLIGHT1, tile.coord)
                elif tile == self.end:
                    pg.draw.rect(screen, HIGHLIGHT2, tile.coord)
                elif tile == self.selected:
                    pg.draw.rect(screen, HIGHLIGHT2, tile.coord)
                else:
                    tile.draw(screen)
                pg.draw.rect(screen, BACKGROUND, tile.coord, 2)
        pg.display.flip()
        
        
    def set_tile_state(self, x: int, y: int, mode: int) -> None: 
        """ Switches the Orientation of the tile at <x, y> """
        for rows in self.tiles:
            for tile in rows:
                if tile.is_cursor_on(x, y):
                    if mode == 1:  
                        tile.switch(0)
                    elif mode == 2:
                        tile.switch(1)
    
    
    def start_end(self, x: int, y: int, mode: int, end=False) -> None:
        """ Sets the starting and end MazeTile"""
        if mode != 0:
            return 
        
        for rows in self.tiles:
            for tile in rows:
                if tile.is_cursor_on(x, y):
                    if not end:
                        self.start = tile
                    else:
                        self.end = tile
    
    
    def get_children(self, current_tile: MazeTile) -> List[MazeTile]:
        """ Return all the adjacent children of <tile> """
        
        adj = [(0, -1), (0, 1), (-1, 0), (1, 0), 
               (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        children = []
        for new_pos in adj:

            row = current_tile.pos[0] + new_pos[0]
            col = current_tile.pos[1] + new_pos[1]
            
            # Check within maze bounds
            if row < 0 or row >= 40 or col < 0 or col >= 40:
                continue

            tile = self.tiles[row][col]
            
            # Check if on walkable tile
            if tile.val == 0:
                continue
            
            children.append(tile)
            
        return children
    
    
    def solve_astar(self, screen: pg.Surface) -> List[MazeTile]:
        """ Finds the shortest path from start to end """
        
        if self.end is None or self.start is None:
            return self.invalid(screen, "Invalid Start/End Points")
            
        open_lst, closed_lst = [self.start], []
        
        current_tile = None
        while open_lst != [] and current_tile != self.end:
            
            # Event loop to stop it from freezing
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    exit()
            
            # Finding node with the least cost in open
            current_tile = open_lst[0]
            current_i = 0
            for index, item in enumerate(open_lst):
                if item.cost < current_tile.cost:
                    current_tile = item
                    current_i = index 
        
            closed_lst.append(open_lst.pop(current_i))
            
            self.selected = current_tile
            self.draw(screen)
            pg.time.delay(50)
                
            # Getting all the valid adjacent children
            children = self.get_children(current_tile)

            for child in children:   
                
                # If already on the closed_lst
                if child in closed_lst:
                    continue 
                
                # Calculate properties
                dist = current_tile.dist + 1
                heur = ((child.pos[0] - self.end.pos[0]) ** 2) + \
                                    ((child.pos[1] - self.end.pos[1]) ** 2)             
                cost = dist + heur
                
                # If not in open_lst, add it and set properties and move on
                if child not in open_lst:
                    # Setting all the properties of valid children
                    child.parent = current_tile
                    child.dist, child.heur, child.cost = dist, heur, cost
                    open_lst.append(child)
                
                # Else if its in open_lst, update if cost is lower
                else:
                    for open_n in open_lst:
                        if child == open_n and cost < open_n.cost:
                            open_n.parent = current_tile
                            open_n.cost = cost
                            open_n.heur = heur
                            open_n.dist = dist
                    
            pg.display.flip()
        
        # Hit destination
        if current_tile == self.end:
            return self.finish(screen, current_tile)
        # Else ran out of possiblities
        return self.invalid(screen, "Invalid Obstacles")
         
         
    def invalid(self, screen: pg.Surface, text: str) -> None:
        """ Draws the screen when given an invalid input """
        clear_screen(screen)
        border(screen) 
        write_text(screen, "Impossible!", get_font(72), TEXT, (50, 210))
        pg.draw.rect(screen, TEXT, (50, 310, 540, 10))
        time_loop(screen, 5000)
        return [-1]
        
        
    def finish(self, screen: pg.Surface, current_tile: MazeTile) -> List[MazeTile]:
        """ Returns the path after solving it"""
        
        # Getting the final path
        path = []
        while current_tile is not None:
            path.append(current_tile)
            current_tile = current_tile.parent

        # Drawing the final path with obstacles
        clear_screen(screen)          
        for rows in self.tiles:
            for tile in rows:
                if tile in path:
                    pg.draw.rect(screen, HIGHLIGHT2, tile.coord)
                elif tile.val == 1:
                    pg.draw.rect(screen, (105, 105, 105), tile.coord)
                elif tile.val == 0:
                    pg.draw.rect(screen, BACKGROUND, tile.coord)
                pg.draw.rect(screen, BACKGROUND, tile.coord, 2)
        
        pg.display.flip()
        time_loop(screen, 10000)
        
        return path
            
                        
                        
    
                    
        
        
        
if __name__ == '__main__':
    run_astar_vis()
        