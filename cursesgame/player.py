from collections import defaultdict
from interfaces import *
from util import color
from curses import COLOR_YELLOW, A_BOLD

class Player(Cell, Inventory):
    character = '@'
    color = color(COLOR_YELLOW) | A_BOLD


