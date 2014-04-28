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
        raise NotImplementedError()

    def push_cell(self, pos, val):
        pubsub.pub("log", "%s %s" % (pos, val))
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
        if getattr(obj, 'world_pos', None) is None:
            raise Exception("%s does not have a world_pos attribute", obj)

        world_row = obj.world_pos[0] + offset[0]
        world_col = obj.world_pos[1] + offset[1]

        return (world_row, world_col)

