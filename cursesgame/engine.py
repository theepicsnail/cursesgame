import curses
from player import Player
from util import color
from world import World

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

    def mainloop(self):
        char = self.window.getch()
        left = 10
        top = 10
        height, width = self.window.getmaxyx()
        player = Player(15, 15)
        world = World()
        while char != 27:
            self.window.erase()
            top = max(0, player.row - min(world.height, height)/2)
            left = max(0, player.col - min(world.width, width)/2)
            #draw the screen
            for row in xrange(top, top+height):
                if row >= world.height:
                    break
                for col in xrange(left, left+width):
                    if col >= world.width:
                        break
                    try:
                        cell = world.get_cell(row, col)
                        self.window.addstr(row-top, col-left,
                            cell.character.encode('utf-8'), cell.color)
                    except Exception:pass
            self.window.addch(player.row-top, player.col-left, '@',
                    color(curses.COLOR_YELLOW) | curses.A_BOLD)
            self.status.addstr(1, 1, "Pos: {}, {}".format(
                    player.row, player.col))

            for idx, (item, count) in enumerate(player.inventory.items()):
                self.status.addstr(2, 1+4*idx, item.character.encode('utf-8'),
                        item.color)
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
            else:
                continue
            next_loc = tuple(next_loc)

            # collision detection
            # out of bounds
            if next_loc[0] < 0 or\
                next_loc[1] < 0 or\
                next_loc[0] >= world.height or\
                next_loc[1] >= world.width:
                continue

            cell = world.get_cell(next_loc[0], next_loc[1])
            if cell.enterable_by(player):
                player.row, player.col = next_loc
                cell.on_entry(player, world)


