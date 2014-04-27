# -*- coding: utf-8 -*-
import curses
from util import color
from interfaces import *

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

    def on_entry(self, cell, world):
        if isinstance(cell, Inventory) and isinstance(cell, Position):
            cell.add_item(world.pop_cell(*cell.get_pos()))
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

    def enterable_by(self, cell, world, direction):
        if isinstance(cell, Inventory):
            return cell.has_item(self.key)

    def on_entry(self, cell, world):
        cell.rem_item(self.key)
        world.pop_cell(*cell.get_pos())

class DiamondDoor(Door):
    key = Diamond()
    #Specifically no replacement value
    # We're using this as a comparison value, if this goes
    # into the world object, something has gone wrong.

class RedDiamondDoor(Door):
    key = RedDiamond()

class PushableBlock(Cell):
    character = 'X'
    color = color(curses.COLOR_WHITE)
    def enterable_by(self, cell, world, direction):
        if isinstance(cell, Position):
            row, col = cell.get_pos()
            self.dest = row + direction[0]*2,\
                col + direction[1]*2
            if world.peek_cell(*self.dest).enterable_by(self, world, direction):
                return True

    def on_entry(self, cell, world):
        world.push_cell(self.dest[0], self.dest[1],
            world.pop_cell(*cell.get_pos()))

