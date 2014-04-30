import unittest
import sys
import os
# Use fake curses library
sys.path.insert(0, os.path.abspath("test/fakes/fake_curses"))

from cursesgame.cell import *
from cursesgame.player import Player
from cursesgame.world import World


def buildWorld(cells):
    """Given an array of cells, turn it into a world
    You will only be able to move west/east in this world
    the world will have the player placed at (0,0)
    """
    world = World(len(cells), 1)
    for C, cell in enumerate(cells):
        if cell is None:
            continue
        world.push_cell((0, C), cell)
    world.push_cell((0, 0), world.get_player())
    return world


class TestCollisions(unittest.TestCase):
    def testUsingDoorWithKey(self):
        """ [Player] [Key]   [Door]
            to
            [Space]  [Space] [Player]
        """
        self.world = buildWorld([None, Diamond(), DiamondDoor()])

        self.world.move_east(self.world.get_player(), 2)
        self.assertEqual((0, 2), self.world.at(self.world.get_player()))

    def testPushingBlock(self):
        """ [Player] [Block]  [Space]
            to
            [Space]  [Player] [Block]
        """
        block = PushableBlock()
        self.world = buildWorld([None, block, None])

        self.world.move_east(self.world.get_player())

        self.assertEqual((0, 1), self.world.at(self.world.get_player()))
        self.assertEqual((0, 2), self.world.at(block))

    def testPushingMultipleBlocks(self):
        """ [Player] [Block]  [Space] [Block] [Space]
            to
            [Space]  [Player] [Block] [Block] [Space]
            Moving east twice, should first move the block
            then the block should prevent the player from moving
            any more east. (i.e. the player can not move multiple blocks)
        """
        block = PushableBlock()
        block2 = PushableBlock()
        self.world = buildWorld([None, block, Grass(), block2, Grass()])

        self.world.move_east(self.world.get_player())

        self.assertEqual((0, 1), self.world.at(self.world.get_player()))
        self.assertEqual((0, 2), self.world.at(block))
        self.assertEqual((0, 3), self.world.at(block2))

        self.world.move_east(self.world.get_player())

        self.assertEqual((0, 1), self.world.at(self.world.get_player()))
        self.assertEqual((0, 2), self.world.at(block))
        self.assertEqual((0, 3), self.world.at(block2))



if __name__ == '__main__':
   unittest.main()


