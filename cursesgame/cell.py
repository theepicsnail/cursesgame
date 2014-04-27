# -*- coding: utf-8 -*-
import curses
from util import color

class Cell(object):
    """ Cells are the basic unit of the world map
    All items on the map that aren't background are
    cells. Cells are cells, walls are cells, etc.."""

    def __hash__(self):
        return hash(type(self))

    def __eq__(self, other):
        return type(self) == type(other)

    character = ' '
    color = color()
    passable = True
    def enterable_by(self, player, world, direction):
        return self.passable

    def on_entry(self, player, world):
        pass

class CellBuilder(Cell):
    def __eq__(self, other):
        return False

    def setPassable(self, p):
        self.passable = p
        return self

    def setCharacter(self, c):
        self.character = c
        return self

    def setColor(self, c):
        self.color = c
        return self

    def duplicate(self):
        return CellBuilder()\
            .setPassable(self.passable)\
            .setCharacter(self.character)\
            .setColor(self.color)

class Grass(Cell):
    character = 'w'
    color = color(curses.COLOR_GREEN)

class Brick(Cell):
    character = u'▒'
    color = color(curses.COLOR_RED)
    passable = False

class Floor(Cell):
    character = ' '
    color = color()

class Water(Cell):
    character = '~'
    color = color(curses.COLOR_BLUE)
    passable = False

class Bridge(Cell):
    character = u'▓'
    color = color(curses.COLOR_YELLOW)

class Diamond(Cell):
    character = u'♦'
    color = color(curses.COLOR_CYAN) | curses.A_BOLD

    def on_entry(self, player, world):
        player.pickup(world.pop_cell(player.row, player.col))
        return True

    def __unicode__(self):
        return "A shiny, shiny diamond about the size of your head."

class RedDiamond(Diamond):
    color = color(curses.COLOR_RED)

class Door(Cell):
    key = None # This needs over written by subclasses

    def __init__(self):
        self.character = self.key.character
        self.color = self.key.color | curses.A_REVERSE

    def enterable_by(self, player, world, direction):
        if player.has_a(self.key):
            return True

    def on_entry(self, player, world):
        player.drop(self.key)
        world.pop_cell(player.row, player.col)

class DiamondDoor(Door):
    key = Diamond()
    #Specifically no replacement value
    # We're using this as a comparison value, if this goes
    # into the world object, something has gone wrong.

class RedDiamondDoor(Door):
    key = RedDiamond()

class PushableBlock(Cell):
    character = 'X'
    def enterable_by(self, player, world, direction):
        self.dest = player.row + direction[0]*2,\
               player.col + direction[1]*2
        if world.push_cell(*self.dest) == Grass():
            return True
    def on_entry(self, player, world):
        world.push_cell(self.dest[0], self.dest[1],
            world.pop_cell(player.row, player.col))

