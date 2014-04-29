from collections import defaultdict
from interfaces import *
import pubsub
from util import color
from curses import COLOR_YELLOW, A_BOLD

class Player(Cell, Inventory, HP):
    character = '@'
    color = color(COLOR_YELLOW) | A_BOLD
    def set_hp(self, value):
        super(Player, self).set_hp(value)
        pubsub.pub("engine:updateStatus")

    def add_item(self, item):
        super(Player, self).add_item(item)
        pubsub.pub("engine:updateStatus")

    def rem_item(self, item):
        super(Player, self).rem_item(item)
        pubsub.pub("engine:updateStatus")


