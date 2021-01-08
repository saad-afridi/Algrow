import pygame
from sort_functions import SortSteps, InsertionSteps, BubbleSteps, \
    SelectionSteps
import random
from visual_helpers import *

# REMOVE DATA later
# from algrow import HEIGHT, WIDTH, FONT_HEIGHT, VISUALIZE_HEIGHT, \
#     FONT_FAMILY, BACKGROUND, BARS, TEXT, DATA

# Screen Dimensions
HEIGHT, WIDTH = 600, 640
FONT_HEIGHT = 40
VISUALIZE_HEIGHT = HEIGHT - FONT_HEIGHT - 50

# The Randomized List to be visualized and sorted through
DATA = SelectionSteps([random.randint(50, VISUALIZE_HEIGHT) for i in range(32)])


# Text Styling and Colors
# FONT_FAMILY = "Consolas"
# BACKGROUND = (105, 0, 191)
# BARS = (165, 92, 255)
# TEXT = (231, 177, 250)
# # STD_FONT = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)


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
    # render_sort(screen, DATA)
    # #
    # sort_event_loop(screen, DATA)


def selection_screen(screen: pygame.Surface) -> None:
    """
    Selection screen between SEARCHING, SORTING, TITLE
    """
    clear_screen(screen)
    border(screen)
    two_options(screen)

    # Labels
    font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)
    write_text(screen, "Table of Content", font, TEXT, (50, 80))
    write_text(screen, "Sorting", font, BACKGROUND, (250, 285))
    write_text(screen, "Searching", font, BACKGROUND, (235, 475))

    # Separator
    sep_coord = (50, 140, 540, 10)
    pygame.draw.rect(screen, TEXT, sep_coord)

    # TODO: Recognize when clicked on "Searching" and go there
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if 40 < x < 600 and 225 < y < 375:
                    sort_selection(screen)

        pygame.display.flip()


def sort_selection(screen: pygame.Surface) -> None:
    """ The screen that lets you pick what sorting method to
    watch"""

    item = [random.randint(50, VISUALIZE_HEIGHT) for i in range(32)]

    clear_screen(screen)
    border(screen)
    three_options(screen)

    # Labels
    font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)
    write_text(screen, "Bubble Sort", font, BACKGROUND, (230, 100))
    write_text(screen, "Insertion Sort", font, BACKGROUND, (205, 285))
    write_text(screen, "Selection Sort", font, BACKGROUND, (205, 475))

    selected = ""
    while selected == "":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                # Check which box was clicked
                x, y = event.pos
                if 40 < x < 600 and 40 < y < 190:
                    selected = "Bubble"
                    break
                elif 40 < x < 600 and 225 < y < 375:
                    selected = "Insertion"
                    break
                elif 40 < x < 600 and 410 < y < 560:
                    selected = "Selection"
                    break
        pygame.display.flip()

    if selected == "Bubble":
        data = BubbleSteps(item)
    elif selected == "Insertion":
        data = InsertionSteps(item)
    else:
        data = SelectionSteps(item)

    render_sort(screen, data)
    sort_event_loop(screen, data)


def render_sort(screen: pygame.Surface, data: SortSteps) -> None:
    """
    Renders the elements in a list and a text display to the
    screen
    """
    clear_screen(screen)

    # Draw all the elements in list
    _render_data(screen, data)

    # Write the text
    _render_text(screen, data)

    pygame.display.flip()


def _render_data(screen: pygame.Surface, data: SortSteps) -> None:
    """
    Draw all the elements in data

    ==== Precondition ====
    - len(data.items) = 32
    """
    x = 5
    comp = WIDTH // len(data.items)

    for i, elem in enumerate(data.items):
        rect = (x + (i * comp), HEIGHT - elem, 10, elem - 25)
        highlight = _exist_color(i, data)
        if highlight[0]:
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


def _render_text(screen: pygame.Surface, data: SortSteps) -> None:
    """
    Renders the text at the top of the screen
    """
    font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)
    small_font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 23)

    # Separator
    sep_coord = (40, HEIGHT - VISUALIZE_HEIGHT - 20, WIDTH - 80, 5)
    pygame.draw.rect(screen, TEXT, sep_coord)

    # Title, Steps, Cycle
    write_text(screen, data.get_title() + " Sort", font, TEXT,
               (40, (HEIGHT - VISUALIZE_HEIGHT - 10) // 2 - 10))
    write_text(screen, "Step(s):" + str(data.step), small_font, TEXT,
               (10, HEIGHT - 20))
    write_text(screen, "Cycle: " + str(data.cycle), small_font, TEXT,
               (WIDTH - 90, HEIGHT - 20))


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
    pygame.time.wait(1000)

    clear_screen(screen)
    border(screen)

    # Labels
    font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)
    write_text(screen, data.get_title() + " Sort " + "Statistics",
               font, TEXT, (50, 80))
    write_text(screen, "Step(s): " + str(data.step), font, TEXT, (50, 285))
    write_text(screen, "Cycle: " + str(data.cycle), font, TEXT, (50, 475))

    # Separator
    sep_coord = (50, 140, 540, 10)
    pygame.draw.rect(screen, TEXT, sep_coord)

    clock = pg.time.Clock()
    time_elapsed = 0
    while True:
        dt = clock.tick()
        time_elapsed += dt

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pygame.quit()
                exit()

        if time_elapsed > 6000:
            break

        pg.display.flip()

    selection_screen(screen)


if __name__ == '__main__':
    run_visualization()
