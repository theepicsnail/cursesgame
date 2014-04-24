import curses
import math
from player import Player
from cell import *
from util import color
def build_world():
    world = {"height": 100, "width":100}
    world["default"] = Grass()
    #build a 'house'
    for i in xrange(10, 20):
        for j in xrange(11, 20):
            world[(i, j)] = Floor()
        world[(i, 10)] = Brick()
        world[(i, 20)] = Brick()
        world[(10, i)] = Brick()
        world[(20, i)] = Brick()
    world[(20, 15)] = Floor() # Poke a hole for a door

    world[(90, 90)] = Diamond()
    world[(25, 25)] = Diamond()
    world[(25, 26)] = Diamond()
    world[(25, 27)] = Diamond()
    world[(25, 28)] = Diamond()
    world[(25, 29)] = RedDiamond()

    for row in xrange(0, world["height"]):
        for col in xrange(int(math.sin(row/5.0)*3+50), int(math.sin(row/7.0)*4 + 60)):
            world[(row, col)] = Water()

    for col in xrange(50, 58):
        world[(36, col)] = Bridge()
        world[(37, col)] = Bridge()
        world[(72, col)] = Bridge()
        world[(73, col)] = Bridge()
    return world

class Engine:
    def __init__(self):
        self._buildScreens()
        self._showIntro()

    def _buildScreens(self):
        self.screen = curses.newwin(0, 0, 0, 0)

        # rows:4, cols:auto, top:0, left:0
        self.status = self.screen.subwin(4, 0, 0, 0)
        self.status.border(0, 0, 0, 0, 0, 0, 0, 0)

        # rows:auto, cols: auto, top:4, left:0
        self.window = self.screen.subwin(0, 0, 4, 0)
        self.window.keypad(1)

    def _showIntro(self):
        self.window.addstr(0, 0, "Press escape to quit")
        self.window.addstr(1, 0, "Use arrow keys to move")
        self.window.addstr(3, 0, "Press any key to start")
        self.window.getch()

    def mainloop(self,):
        char = self.window.getch()
        left = 10
        top = 10
        height, width = self.window.getmaxyx()
        player = Player(15, 15)
        world = build_world()
        world_height, world_width = world['height'], world['width']
        while char != 27:
            self.window.erase()
            top = max(0, player.row - min(world_height, height)/2)
            left = max(0, player.col - min(world_width, width)/2)
            #draw the screen
            for row in xrange(top, top+height):
                if row >= world_height:
                    break
                for col in xrange(left, left+width):
                    if col >= world_width:
                        break
                    try:
                        if (row, col) in world:
                            cell = world[(row, col)]
                        else:
                            cell = world["default"]

                        self.window.addstr(row-top, col-left,
                            cell.character.encode('utf-8'), cell.color)
                    except:pass
            self.window.addch(player.row-top, player.col-left, '@', color(curses.COLOR_YELLOW) | curses.A_BOLD)
            self.status.addstr(1, 1, "Pos: {}, {}".format(player.row, player.col))

            for idx, (item, count) in enumerate(player.inventory.items()):
                self.status.addstr(2, 1+4*idx, item.character.encode('utf-8'), item.color)
                self.status.addstr("{:<3}".format(count))
            self.status.refresh()

            #handle input
            char = self.window.getch()
            next_loc = [player.row, player.col]
            if char == 258: # Down
                next_loc[0] += 1
            elif char == 259: # Up
                next_loc[0] -= 1
            elif char == 260: # left
                next_loc[1] -= 1
            elif char == 261: # right
                next_loc[1] += 1
            next_loc = tuple(next_loc)

            # collision detection
            # out of bounds
            if next_loc[0] < 0 or\
                next_loc[1] < 0 or\
                next_loc[0] >= world_height or\
                next_loc[1] >= world_width:
                continue
            if next_loc in world:
                old_loc = (player.row, player.col)
                player.row, player.col = next_loc
                if not world[next_loc].on_collision(player, world):
                    player.row, player.col = old_loc
                    continue

            player.row, player.col = next_loc


