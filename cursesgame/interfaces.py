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

    def __str__(self):
        return type(self).__name__

    def get_cell_char(self):
        return self.character

    def get_cell_color(self):
        return self.color

    def enterable_by(self, cell, world, direction):
        return self.passable

    def before_entry(self, cell, world):
        pass

    def after_exit(self, cell, world):
        pass

class Inventory(object):
    def __init__(self):
        super(Inventory,self).__init__()
        self._inventory = defaultdict(int)

    def add_item(self, item):
        self._inventory[item] += 1

    def rem_item(self, item):
        if self._inventory[item] <= 0:
            raise Exception("Item not in inventory: %s" % item)

        self._inventory[item] -= 1

        if self._inventory[item] <= 0:
            del self._inventory[item]

    def has_item(self, item):
        return item in self._inventory

    def list_items(self):
        return self._inventory.iteritems()

class HP(object):
    def __init__(self):
        super(HP, self).__init__()
        self._health = 0

    def set_hp(self, value):
        self._health = value

    def get_hp(self):
        return self._health

    def inc_hp(self, value):
        self._health += value

    def dec_hp(self, value):
        self._health -= value
