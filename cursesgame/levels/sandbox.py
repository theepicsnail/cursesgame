from cell import *
import world
from player import Player

class World(world.World):
    def create(self):
        tiles = [ Grass, Brick, Floor, Water, Bridge, Scroll, Diamond, \
        RedDiamond, DiamondDoor, RedDiamondDoor, PushableBlock]

        self.width =  len(tiles) + 1
        self.height = 1

        for i in xrange(len(tiles)):
            self.push_cell((0, i+1), tiles[i]())

        self.push_cell((0, 0), self.player)

