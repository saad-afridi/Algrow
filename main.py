import pygame

from sort_functions import SortSteps, InsertionSteps, BubbleSteps, \
    SelectionSteps
import random
from visual_helpers import *
from sudoku_visual import *
from astar_visual import *


def run_visualization() -> None:
    """
    Displays an interactive graphical display of sorting
    algorithms
    """
    pygame.init()
    pygame.display.set_caption('Algrow')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    title_screen(screen)

    selection_screen(screen)


def selection_screen(screen: pygame.Surface) -> None:
    """
    Selection screen between SEARCHING, SORTING, TITLE
    """
    clear_screen(screen)
    border(screen)

    # Labels
    draw_header(screen, "Table of Content")
    b1 = PButton(screen, (180, 230, 300, 50))
    b1.add_text("Sorting")
    b2 = PButton(screen, (180, 300, 300, 50))
    b2.add_text("Searching")
    buttons = [b1 ,b2]
    
    # TODO: Recognize when clicked on "Searching" and go there
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if b1.is_cursor_on((x, y), True):
                    sort_selection(screen)
                if b2.is_cursor_on((x, y), True):
                    search_selection(screen)
        
        for b in buttons:
            if b.is_cursor_on(pygame.mouse.get_pos()):
                b.hover()
            else:
                b.draw()

        pygame.display.flip()


def sort_selection(screen: pygame.Surface) -> None:
    """ The screen that lets you pick what sorting method to
    watch"""

    # The list to sort
    item = [random.randint(50, VISUALIZE_HEIGHT) for i in range(32)]

    clear_screen(screen)
    border(screen)
    draw_header(screen, "Types of Sorting Algorithms")

    # Labels
    bubble = PButton(screen, (155, 230, 350, 50))
    bubble.add_text("Bubble Sort")
    insert = PButton(screen, (155, 330, 350, 50))
    insert.add_text("Insertion Sort")
    select = PButton(screen, (155, 430, 350, 50))
    select.add_text("Selection Sort")
    buttons = [bubble, insert, select]
    
    selected = ""
    while selected == "":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                # Check which box was clicked
                x, y = event.pos
                if bubble.is_cursor_on((x, y), True):
                    selected = "Bubble"
                elif insert.is_cursor_on((x, y), True):
                    selected = "Insertion"
                elif select.is_cursor_on((x, y), True):
                    selected = "Selection"
        
        for b in buttons:
            if b.is_cursor_on(pygame.mouse.get_pos()):
                b.hover()
            else:
                b.draw()
            
        pygame.display.flip()

    if selected == "Bubble":
        data = BubbleSteps(item)
    elif selected == "Insertion":
        data = InsertionSteps(item)
    else:
        data = SelectionSteps(item)

    render_sort(screen, data)
    sort_event_loop(screen, data)


def search_selection(screen: pygame.Surface) -> None:
    """ The screen that lets you pick what searching algorithm to
    watch"""

    clear_screen(screen)
    border(screen)
    draw_header(screen, "Types of Searching Algorithms")

    # Labels
    backtrack = PButton(screen, (155, 230, 350, 50))
    backtrack.add_text("BackTracking")
    astar = PButton(screen, (155, 330, 350, 50))
    astar.add_text("A*")
    buttons = [backtrack, astar]
    
    selected = ""
    while selected == "":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                # Check which box was clicked
                x, y = event.pos
                if backtrack.is_cursor_on((x, y), True):
                    selected = "Backtrack"
                elif astar.is_cursor_on((x, y), True):
                    selected = "A*"
        
        for b in buttons:
            if b.is_cursor_on(pygame.mouse.get_pos()):
                b.hover()
            else:
                b.draw()
            
        pygame.display.flip()

    if selected == "Backtrack":
        solve_sudoku_GUI(screen)
    elif selected == "A*":
        render_astar_vis(screen)
    
    
# ============================= SORTING VISUALISATION METHODS ====================
def render_sort(screen: pygame.Surface, data: SortSteps) -> None:
    """
    Renders the elements in a list and a text display to the
    screen
    """
    clear_screen(screen)
    border(screen)
    
    # Write the text
    _render_text(screen, data)
    
    # Draw all the elements in list
    _render_data(screen, data)  

    pygame.display.flip()


def _render_text(screen: pygame.Surface, data: SortSteps) -> None:
    """
    Renders the text at the top of the screen
    """
    small_font = get_font(20)
    draw_header(screen, data.get_title() + " Sort")

    # Steps, Cycle
    write_text(screen, "Step(s):" + str(data.step), small_font, TEXT,
               (48, HEIGHT - 25))
    write_text(screen, "Cycle(s): " + str(data.cycle), small_font, TEXT,
               (WIDTH - 120, HEIGHT - 25))
    

def _render_data(screen: pygame.Surface, data: SortSteps) -> None:
    """
    Draw all the elements in data

    ==== Precondition ====
    - len(data.items) = 32
    """
    x = 50
    comp = (WIDTH - 96) // len(data.items)

    for i, elem in enumerate(data.items):
        rect = (x + (i * comp), HEIGHT - elem, 10, elem - 25)
        highlight = _exist_color(i, data)
        if highlight[0] and not data.complete():
            pygame.draw.rect(screen, highlight[1], rect)
        else:
            pygame.draw.rect(screen, BARS, rect)


def _exist_color(n: int, data: SortSteps):
    """
    Return whether n is an index being compared in data
    if yes, return it's color too. Otherwise, return False and an empty
    Tuple
    """
    index = -1
    for tup in data.indices:
        if n in tup:
            index = tup.index(n)

    if index == -1:
        return False, ()
    if index == 0:
        return True, tup[2]
    return True, tup[-1]


def sort_event_loop(screen: pygame.Surface, data: SortSteps) -> None:
    """
    Update display or respond to events (mouse clicks, key presses)
    """
    time_elapsed = 0
    clock = pygame.time.Clock()

    timer = 25
    paused = False
    while True:
        dt = clock.tick()

        time_elapsed += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                paused = not paused

        if data.complete() and not paused:
            sort_end(screen, data)

        if time_elapsed > timer and not paused:
            data.iterate()
            time_elapsed = 0

        render_sort(screen, data)

def sort_end(screen: pygame.Surface, data: SortSteps) -> None:
    """
    Once it's finished sorting
    """
    pygame.time.wait(2000)

    clear_screen(screen)
    border(screen)

    # Labels
    draw_header(screen, data.get_title() + " Sort" + " Statistics")
    write_text(screen, "Step(s): " + str(data.step), get_font(), TEXT, (50, 285))
    write_text(screen, "Cycle: " + str(data.cycle), get_font(), TEXT, (50, 475))

    time_loop(screen, 6000)
    selection_screen(screen)
    

# ========================== BACKTRACKING AND ASTAR ================================
def solve_sudoku_GUI(screen: pg.Surface) -> None:
    """ Solve sudoku using backtracking algorithm and display
    it on GUI """
    
    clear_screen(screen)
    board = SudokuBoard()
    board.draw(screen)
    done = False
    while not done:
        
        for e in pg.event.get():
            if e.type == pg.QUIT:
                selection_screen(screen)
            
        done = board.solve(screen)

        board.draw(screen)
        pg.display.flip()
    
    board.finished(screen)
    time_loop(screen, 8000)
    selection_screen(screen)


def render_astar_vis(screen: pygame.Surface) -> None:
    """ Render the astar simulation program """
 
    board = Maze()
    board.draw(screen)
    
    # Mode 0 is for selecting start, end pts
    # Mode 1 is for creating obstacles
    # Mode 2 is for clearing obstacles
    mode, ans = 0, []
    while ans == []:
        
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit()
            
            # If a key is pressed
            if e.type == pg.KEYUP:
                
                # Left Shift for adding obstacles
                if e.key == pg.K_LSHIFT:
                    if mode != 1:
                        mode = 1
                    else:
                        mode = 0
                
                # Capslock for clearing obstacles
                if e.key == pg.K_CAPSLOCK:
                    if mode != 2:
                        mode = 2
                    else:
                        mode = 0
                
                # Space to start simulation
                if e.key == pg.K_SPACE:
                    ans = board.solve_astar(screen)
            
            # If clicked with mouse
            if e.type == pg.MOUSEBUTTONDOWN and mode == 0:
                x, y = pg.mouse.get_pos()
                if e.button == 1:
                    board.start_end(x, y, mode)
                
                elif e.button == 3:
                    board.start_end(x, y, mode, True)
                    
                    
        x, y = pg.mouse.get_pos()
        board.set_tile_state(x, y, mode)
        
        if not ans:
            board.draw(screen)
            pg.display.flip()
    
    selection_screen(screen)
    
    
if __name__ == '__main__':
    run_visualization()
