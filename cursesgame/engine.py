import curses
from player import Player
from util import color
from world import World

class Engine:
    def __init__(self):
        self._buildScreens()
        self._showIntro()
        self.player = Player()

    def _buildScreens(self):
        self.screen = curses.newwin(0, 0, 0, 0)

        # rows:4, cols:auto, top:0, left:0
        self.status = self.screen.subwin(4, 0, 0, 0)

        # rows:auto, cols: auto, top:4, left:0
        self.window = self.screen.subwin(0, 0, 4, 0)
        self.window.keypad(1)

    def _showIntro(self):
        self.window.addstr(0, 0, "Press escape to quit")
        self.window.addstr(1, 0, "Use arrow keys to move")
        self.window.addstr(3, 0, "Press any key to start")

    def mainloop(self):
        char = self.window.getch()
        left = 10
        top = 10
        height, width = self.window.getmaxyx()
        import levels.level1
        world = levels.level1.Level1()
        player = world.get_player()

        while char != 27:
            self.window.erase()
            for row in xrange(-height/2, height/2):
                for col in xrange(-width/2, width/2):
                    try:
                        cell = world.peek_cell(
                            world.relative_to(player, (row, col)))
                        self.window.addstr(row - - height/2, col - - width/2,
                            #row - -height/2, col - -width/2,
                            cell.character.encode('utf-8'), cell.color)
                    except: pass


            #self.window.addch(player_loc[0]-top, player_loc[1]-left, '@',
            #        color(curses.COLOR_YELLOW) | curses.A_BOLD)

            # draw status bar
            self.status.erase()
            self.status.border(0, 0, 0, 0, 0, 0, 0, 0)
            #self.status.addstr(1, 1, "Pos: {}".format(player_loc))
            for idx, (item, count) in enumerate(player.list_items()):
                self.status.addstr(2, 1+4*idx, item.character.encode('utf-8'),
                        item.color)
                self.status.addstr("{:<3}".format(count))
            self.status.refresh()

            #handle input
            char = self.window.getch()
            if char == 258: # Down
                direction = (1, 0)
            elif char == 259: # Up
                direction = (-1, 0)
            elif char == 260: # left
                direction = (0, -1)
            elif char == 261: # right
                direction = (0, 1)
            else:
                continue
            next_loc = world.relative_to(player, direction)
            #map(sum, zip(player_loc, direction))

            # collision detection
            # out of bounds
            if next_loc[0] < 0 or\
                next_loc[1] < 0 or\
                next_loc[0] >= world.height or\
                next_loc[1] >= world.width:
                continue

            cell = world.peek_cell(next_loc)
            if cell.enterable_by(player, world, direction):
                pos = world.at(player)
                val = world.pop_cell(pos)

                world.push_cell(next_loc, val)
                cell.on_entry(player, world)


