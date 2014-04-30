from collections import defaultdict
from cell import *
from player import Player
import math
import util
import curses # For colors only
import pubsub

class World(object):
    def __init__(self, width=100, height=100, default=Grass()):
        self.width = width
        self.height = height
        self.default = default
        self.cells = defaultdict(list)
        self.player = Player()
        self.create()

    def create(self):
        """ This should be overwritten by subclasses to create their world"""
        pass

    def push_cell(self, pos, val):
        if getattr(val, 'world_pos', None) is not None:
            raise Exception("Cell %s already exists at %s" %(val, val.world_pos))
        assert(val is not None)

        val.world_pos = pos
        self.cells[pos].append(val)

    def pop_cell(self, (row, col)):
        val = self.cells[(row, col)].pop()
        val.world_pos = None
        return val

    def peek_cell(self, pos):
        if self.contains_location(pos):
            if not self.cells[pos]:
                return self.default
            return self.cells[pos][-1]
        return None

    def get_player(self):
        return self.player

    def contains_location(self, (row, col)):
        if (0 <= row < self.height) and (0 <= col < self.width):
            return True
        return False

    # Get positions by relative position
    def at(self, obj):
        return self.relative_to(obj)
    def west_of(self, obj, count=1):
        return self.relative_to(obj, (0, -count))
    def east_of(self, obj, count=1):
        return self.relative_to(obj, (0, count))
    def north_of(self, obj, count=1):
        return self.relative_to(obj, (-count, 0))
    def south_of(self, obj, count=1):
        return self.relative_to(obj, (count, 0))
    def relative_to(self, obj, offset=(0,0)):
        if type(obj) == tuple:
            return (obj[0] + offset[0], obj[1] + offset[1])

        if getattr(obj, 'world_pos', None) is None:
            raise Exception("%s does not have a world_pos attribute", obj)

        world_row = obj.world_pos[0] + offset[0]
        world_col = obj.world_pos[1] + offset[1]

        return (world_row, world_col)

    # Move cells around the map
    def move_north(self, cell, count=1):
        moved = self._move_cell(cell, (-1, 0))
        if moved and count > 1:
            self.move_north(cell, count-1)
        return moved

    def move_south(self, cell, count=1):
        moved = self._move_cell(cell, (1, 0))
        if moved and count > 1:
            self.move_south(cell, count-1)
        return moved

    def move_west(self, cell, count=1):
        moved = self._move_cell(cell, (0, -1))
        if moved and count > 1:
            self.move_west(cell, count-1)
        return moved

    def move_east(self, cell, count=1):
        moved =  self._move_cell(cell, (0, 1))
        if moved and count > 1:
            self.move_east(cell, count-1)
        return moved

    def _move_cell(self, cell, direction):
        """Attempt to move a cell in a given direction
        If it can't move that way, this method is a noop

        Returns whether the world has changed
        """
        next_loc = self.relative_to(cell, direction)
        neighbor = self.peek_cell(next_loc)

        if neighbor is None: # Off map
            return False

        if neighbor.enterable_by(cell, self, direction):
            # Hooray, we can move <cell> <direction>!
            old_loc = self.at(cell)
            # The cell we remove should be us
            assert(self.pop_cell(old_loc) == cell)

            exposed_cell = self.peek_cell(old_loc)
            if exposed_cell is not None:
                exposed_cell.after_exit(cell, self)

            neighbor.before_entry(cell, self)
            self.push_cell(next_loc, cell)
            return True

        return False



