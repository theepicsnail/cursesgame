from cell import *
import math

class World:
    def __init__(self):
        self.width = 100
        self.height = 100
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
        self.cells[(20, 15)] = Floor() # Poke a hole for a door

        self.cells[(90, 90)] = Diamond()
        self.cells[(25, 25)] = Diamond()
        self.cells[(25, 26)] = Diamond()
        self.cells[(25, 27)] = Diamond()
        self.cells[(25, 28)] = Diamond()
        self.cells[(25, 29)] = RedDiamond()

        for row in xrange(0, self.height):
            for col in xrange(int(math.sin(row/5.0)*3+50), int(math.sin(row/7.0)*4 + 60)):
                self.cells[(row, col)] = Water()

        for col in xrange(50, 58):
            self.cells[(36, col)] = Bridge()
            self.cells[(37, col)] = Bridge()
            self.cells[(72, col)] = Bridge()
            self.cells[(73, col)] = Bridge()

    def get_cell(self, row, col):
        return self.cells.get((row, col), self.default)

    def remove_cell(self, row, col):
        if (row, col) in self.cells:
            del self.cells[(row, col)]
        else:
            raise Exception("No item to delete at (%s, %s)" % (row, col))

