"""
Implementing sorting classes for the sorting visualiser in main.py,
currently implemented:
QuickSort, InsertionSort, BubbleSort
"""

from typing import List, Tuple, Dict
import random

HIGHLIGHT1 = (125, 255, 186)
HIGHLIGHT2 = (52, 219, 235)


class SortSteps:
    """
    A step in a sorting algorithm that is compatible with
    the sort visualiser

    ==== Public Attributes ===
    items: the current state of the list
    index: the current item being evaluated
    step: the number of steps it took to reach the state in [items]
    cycle: the number of time restarted search
    indices: all the indices that are being compared, stored in a
            list

    ==== Private Attributes ====
    _ans: the sorted version of items
    """
    items: List[int]
    index: int
    step: int
    _ans: List[int]
    cycle: int
    indices: List[Tuple]

    def __init__(self, data: List[int]):
        """
        Initialize a SortSteps object
        """
        self.items = data
        self.index = 0
        self.step = 0
        self._ans = sorted(data)
        self.cycle = 0
        self.indices = [()]

    def iterate(self):
        """One iteration of said sorting algorithm for visualiser"""
        raise NotImplementedError

    def get_title(self) -> str:
        """Return the name of this sorting algorithm"""
        raise NotImplementedError

    def complete(self):
        """Return whether the sorting is complete"""
        return self._ans == self.items

    def __str__(self):
        """Return the string representation of a SortSteps object"""
        return "data: " + str(self.items) + "\nsteps: " + str(self.step) \
               + "\nindex: " + str(self.index)


class BubbleSteps(SortSteps):

    def iterate(self):

        if self.complete():
            return

        self.step += 1

        # When at last element, reset
        if self.index == len(self.items) - 1:
            self.index = 0

        # Swap elements
        if self.items[self.index] > self.items[self.index + 1]:
            self.items[self.index], self.items[self.index + 1] = \
                self.items[self.index + 1], self.items[self.index]

        # Updating Indices affected
        self.indices[0] = (self.index, self.index + 1, HIGHLIGHT1, HIGHLIGHT2)

        # Updating Cycle, Index
        self.index += 1
        self.cycle = self.step // len(self.items)

    def get_title(self) -> str:
        return "Bubble"


class InsertionSteps(SortSteps):
    compare: int

    def __init__(self, data: List[int]):
        super().__init__(data)
        self.compare = 0

    def iterate(self):

        if self.complete():
            return

        self.step += 1
        self.indices[0] = (self.compare, self.index, HIGHLIGHT1, HIGHLIGHT2)

        # Check if it has predecessors
        if self.compare >= self.index:
            self.index += 1
            self.compare = 0

        # elif found a place for the current item
        elif self.items[self.compare] > self.items[self.index]:
            tmp = self.items[self.index]
            del self.items[self.index]
            self.items.insert(self.compare, tmp)
            self.compare = 0
            self.index += 1

        # compare with a diff element
        else:
            self.compare += 1

    def get_title(self) -> str:
        return "Insertion"


class SelectionSteps(SortSteps):
    low: Tuple

    def __init__(self, data: List[int]):
        super().__init__(data)
        self.low = (float('inf'), -1)

    def iterate(self):
        if self.complete():
            return

        self.step += 1

        if self.low[1] != -1:
            self.indices[0] = (self.low[1], self.index, HIGHLIGHT2, HIGHLIGHT1)

        # if index reached
        if self.index == len(self.items):
            # Insert found min
            self.items.insert(self.cycle, self.low[0])
            del self.items[self.low[1] + 1]
            self.cycle += 1
            self.index = self.cycle
            self.low = (float('inf'), -1)

        if self.items[self.index] < self.low[0]:
            self.low = self.items[self.index], self.index

        self.index += 1

    def get_title(self) -> str:
        return "Selection"


class MergeSteps(SortSteps):

    def __init__(self, data: List[int]):
        super().__init__(data)
        self.rec_depth = 0

    def iterate(self):
        # steps = 32 x 4 = 128
        self.step += 1
        # [0, 1, 4, 3]
        # I want to compare(0, 1) and compare(4, 3)
        if self.index >= len(self.items):
            self.cycle += 1
            self.rec_depth += 1

    #     if self.index + self.rec_depth < len(self.items) - 2:
    #         self.inde
    #
    # def _merge(self, a: List[int], b: List[int]) -> :

    def get_title(self) -> str:
        return "Merge"


def _color_generator() -> Tuple:
    """
    Returns a random colour represented as a tuple (r, g, b)
    """
    a = random.randint(75, 200)
    b = random.randint(75, 200)
    c = random.randint(75, 200)
    return a, b, c


if __name__ == "__main__":

    ins = SelectionSteps([3, 1, 2, 82, 3, 5, 82])

    copy = [elem for elem in ins.items]
    copy.sort()
    # ans = [1, 2, 3, 3, 5, 82, 82]
    print(ins)
    while not ins.complete():
        ins.iterate()
        print(ins)
