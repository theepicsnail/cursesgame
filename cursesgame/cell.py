# -*- coding: utf-8 -*-
import curses
from util import color
from interfaces import *
from player import Player
import pubsub

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

class Scroll(Cell):
    character = u'ʃ'
    color = color(curses.COLOR_CYAN)

    def before_entry(self, cell, world):
        if isinstance(cell, Inventory):
            cell.add_item(world.pop_cell(world.at(self)))
            pubsub.pub("log", "You picked up a scroll")

class Diamond(Cell):
    character = u'♦'
    color = color(curses.COLOR_CYAN) | curses.A_BOLD

    def before_entry(self, cell, world):
        if isinstance(cell, Inventory):
            # remove self from the world
            # Add it to cells's inventory
            cell.add_item(world.pop_cell(world.at(self)))
            pubsub.pub("log", "You pick up a key")
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
            if cell.has_item(self.key):
                return True
            pubsub.pub("log", "The door is locked.")

    def before_entry(self, cell, world):
        cell.rem_item(self.key)
        world.pop_cell(world.at(self))
        pubsub.pub("log", "You unlock the door")

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
        if not isinstance(cell, Player):
            return False

        self.dest = world.relative_to(cell, direction)
        self.dest = world.relative_to(self.dest, direction)
        if world.peek_cell(self.dest).enterable_by(self, world, direction):
            return True


    def before_entry(self, cell, world):
        world.push_cell(self.dest, world.pop_cell(world.at(self)))

