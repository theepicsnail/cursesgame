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
        self.player = Player(0,0)

    def checkPassable(self, cls, expected):
        world = {(0, 0): cls()}
        success = world[(0, 0)].on_collision(self.player, world)
        self.assertTrue(success == expected)

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

