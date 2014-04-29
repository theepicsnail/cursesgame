import unittest
import sys
from cStringIO import StringIO
import os

# Use fake curses library
sys.path.insert(0, os.path.abspath("test/fakes/fake_curses"))

from cursesgame.player import Player
from cursesgame.cell import *

class TestCollisions(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def checkPassable(self, cls, expected):
        world = {(0, 0): cls()}
        #Entering from the left
        success = world[(0, 0)].enterable_by(self.player, world, (0,1))
        self.assertTrue(success == expected)

    def testGrassIsPassable(self):
        self.checkPassable(Grass, True)

    def testBrickIsNotPassable(self):
        self.checkPassable(Brick, False)

    def testFloorIsPassable(self):
        self.checkPassable(Floor, True)

    def testWaterIsNotPassable(self):
        self.checkPassable(Water, False)

    def testBridgeIsPassable(self):
        self.checkPassable(Bridge, True)

    def testDiamondIsPassable(self):
        self.checkPassable(Diamond, True)

    def testRedDiamondIsPassable(self):
        self.checkPassable(RedDiamond, True)

class TestHash(unittest.TestCase):
    def testDiamondHashes(self):
        self.assertFalse(hash(Diamond()) == hash(RedDiamond()))
        self.assertTrue(hash(Diamond()) == hash(Diamond()))
        self.assertTrue(hash(RedDiamond()) == hash(RedDiamond()))


if __name__ == '__main__':
   unittest.main()

