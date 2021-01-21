
from typing import Tuple, Optional, Any, List

ADJ = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

class _Node:
    
    parent: Any
    pos: Optional[Tuple[int]]
    cost: int 
    dist: int
    heur: int
    
    def __init__(self, parent=None, pos=None) -> None:
        """ Initalize a _Node object """
        self.parent = parent
        self.pos = pos
        
        self.cost = 0
        self.dist = 0
        self.heur = 0
        
    def __eq__(self, other: object) -> bool:
        """ Return whether other is equal to self """
        return self.pos == other.pos
        

def astar(maze: List[List[int]], start: Tuple[int], 
          end: Tuple[int]) -> List[Tuple]:
    """ Returns a path from <start> to <end> as a List
    of Tuples """
    
    start_n = _Node(pos=start)
    end_n = _Node(pos=end)
    
    open_lst, close_lst = [], []
    
    open_lst.append(start_n)
    
    while len(open_lst) > 0:
        
        # Getting the lowest cost 
        current_n = open_lst[0]
        current_i = 0
        for index, item in enumerate(open_lst):
            if item.cost < current_n.cost:
                current_n = item
                current_i = index 
        
        close_lst.append(open_lst.pop(current_i))
        
        if current_n == end_n:
            path = []
            current = current_n
            while current is not None:
                path.append(current.pos)
                current = current.parent
            return path[::-1]

        # Getting all the children nodes (adjacent)
        children = []
        for new_pos in ADJ:
            
            node_p = (current_n.pos[0] + new_pos[0], 
                      current_n.pos[1] + new_pos[1])
            
            # Check within maze bounds
            if node_p[0] > (len(maze) - 1) or node_p[0] < 0 \
            or node_p[1] < 0 or node_p[1] > (len(maze) - 1):
                continue
            
            # Check if on walkable tile
            if maze[node_p[0]][node_p[1]] != 0:
                continue
            
            new_n = _Node(current_n, node_p)
            children.append(new_n)
        
        #
        for child in children:
            
            for close_child in close_lst:
                if child == close_child:
                    continue
            
            child.dist = current_n.dist + 1
            child.heur = ((child.pos[0] - end_n.pos[0]) ** 2) + \
                            ((child.pos[1] - end_n.pos[1]) ** 2)
                             
            child.cost = child.dist + child.heur
            
            for open_n in open_lst:
                if child == open_n and child.dist > open_n.dist:
                    continue 
            
            open_lst.append(child)
                    
            
            
            
            
            
            
 
        
if __name__ == '__main__':
    
    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    start = (0, 0)
    end = (7, 6)
    
    path = astar(maze, start, end)
    print(path)
    