""" Base classes for the objects used in this game"""
from collections import defaultdict

class Cell(object):
    """ Base class for items shown on the screen """
    color = None
    character = ' '
    passable = True

    def __hash__(self):
        return hash(type(self))

    def __eq__(self, other):
        return type(self) == type(other)

    def get_cell_char(self):
        return self.character

    def get_cell_color(self):
        return self.color

    def enterable_by(self, cell, world, direction):
        return self.passable

    def on_entry(self, cell, world):
        pass

class Position(object):
    """ Items that have position, at the moment it's only the player"""
    def __init__(self, row=0, col=0):
        super(Position,self).__init__()
        self.row = row
        self.col = col

    def set_pos(self, row, col):
        # For pubsub, this might push a couple messages
        # exiting self.row/col, and entering new row/col
        self.row = row
        self.col = col

    def get_pos(self):
        return (self.row, self.col)

class Inventory(object):
    def __init__(self):
        super(Inventory,self).__init__()
        self.inventory = defaultdict(int)

    def add_item(self, item):
        self.inventory[item] += 1

    def rem_item(self, item):
        if self.inventory[item] <= 0:
            raise Exception("Item not in inventory: %s" % item)

        self.inventory[item] -= 1

        if self.inventory[item] <= 0:
            del self.inventory[item]

    def has_item(self, item):
        return item in self.inventory

    def list_items(self):
        return self.inventory.iteritems()
