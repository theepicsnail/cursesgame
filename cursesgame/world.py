from collections import defaultdict
from cell import *
import math

import util
import curses # For colors only

class World(object):
    def __init__(self, width=100, height=100, default=Grass()):
        self.width = width
        self.height = height
        self.default = default
        self.cells = defaultdict(list)
        self.create()

    def create(self):
        raise NotImplementedError()

    def push_cell(self, row, col, val):
        self.cells[(row, col)].append(val)

    def pop_cell(self, row, col):
        return self.cells[(row, col)].pop()

    def peek_cell(self, row, col):
        if not self.cells[(row, col)]:
            return self.default
        return self.cells[(row, col)][-1]

