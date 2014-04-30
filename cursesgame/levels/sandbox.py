from cell import *
import world
from player import Player

class World(world.World):
    def create(self):
        self.width =  6
        self.height = 3
        self.push_cell((1,1), self.player)
        self.push_cell((1,2), PushableBlock())
        self.push_cell((1,4), PushableBlock())
















