from cell import *
import math

class World:
    def __init__(self):
        self.width = 500
        self.height = 500
        self.default = Grass()
        self.cells = {}

        #build a 'house'
        for i in xrange(10, 20):
            for j in xrange(11, 20):
                self.cells[(i, j)] = Floor()
            self.cells[(i, 10)] = Brick()
            self.cells[(i, 20)] = Brick()
            self.cells[(10, i)] = Brick()
            self.cells[(20, i)] = Brick()
        self.cells[(12, 12)] = Diamond()
        self.cells[(20, 15)] = DiamondDoor()

        self.cells[(25, 29)] = RedDiamond()
        self.cells[(30,30)] = RedDiamondDoor()
        self.cells[(30, 31)] = Diamond()
        self.cells[(30, 32)] = Diamond()
        self.cells[(30, 33)] = Diamond()

        for row in xrange(0, self.height):
            for col in xrange(int(math.sin(row/5.0)*3+50), int(math.sin(row/7.0)*4 + 60)):
                self.cells[(row, col)] = Water()

        for col in xrange(50, 58):
            cell = Bridge()
            if col == 54:
                cell = DiamondDoor()
                cell.replacement = Bridge()

            self.cells[(36, col)] = cell
            self.cells[(37, col)] = cell
            self.cells[(72, col)] = cell
            self.cells[(73, col)] = cell

    def set_cell(self, row, col, val):
        if (row, col) in self.cells:
            raise Exception("(%s, %s) already contains %s" % (
                row, col, self.get_cell(row,col)))

        if val is None:
            raise Exception("Can not set cell to None, use remove_cell")

        self.cells[(row, col)] = val

    def get_cell(self, row, col):
        return self.cells.get((row, col), self.default)

    def remove_cell(self, row, col):
        if (row, col) in self.cells:
            del self.cells[(row, col)]
        else:
            raise Exception("No item to delete at (%s, %s)" % (row, col))

