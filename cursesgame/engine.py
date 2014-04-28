import curses
from player import Player
from util import color
from world import World
import pubsub

class Engine:
    def __init__(self):
        self.side_buffer = []
        self._buildScreens()
        self._showIntro()
        self.player = Player()
        pubsub.sub("log", self.log_message)


    def _buildScreens(self):
        self.screen = curses.newwin(0, 0, 0, 0)

        def add_border(H,W,Y,X):
            screen = curses.newwin(H,W,Y,X)
            screen.border(0,0,0,0,0,0,0,0)
            screen.refresh()
            return screen.derwin(H-2, W-2, 1, 1)

        H,W = self.screen.getmaxyx()
        #
        #     w
        # +---+---------------+
        # |  S  t  a  t  u  s |
        #h+---+---------------+
        # |   |               |
        # | S | window        |
        # | i |               |
        # | d |               |
        # | e |               |
        # |   |               |
        # +---+---------------+
        #
        w = 40
        h = 4
                                #  H W Y X
        self.status = add_border(h, W, 0, 0)
        self.side = add_border(H-h, w, h, 0)
        self.window = add_border(H-h, W-w, h, w)

        self.window.keypad(1)

    def _showIntro(self):
        title = "Super awesome game title"
        self.status.addstr(1,
            (self.status.getmaxyx()[1] - len(title))/2, title,1)

        self.window.addstr(0, 0, "Press escape to quit")
        self.window.addstr(1, 0, "Use arrow keys to move")
        self.window.addstr(2, 0, "Press any key to start")
        self.status.refresh()

    def log_message(self, log):
        self.side_buffer.append(log)

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
                    except Exception:pass

            # draw side bar
            side_row = 0
            log_rows = self.side.getmaxyx()[0]
            for line in self.side_buffer[::-1]:
                if side_row >= log_rows:
                    break
                self.side.addstr(side_row, 0, line[:37], 0)
                side_row += 1

            self.side.refresh()

            # draw status bar
            self.status.erase()
            for idx, (item, count) in enumerate(player.list_items()):
                self.status.addstr(1, 4*idx, item.character.encode('utf-8'),
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
            pubsub.pub("log", "Enter cell: %s" % cell)
            if cell.enterable_by(player, world, direction):
                pubsub.pub("log", "Enterable")
                pos = world.at(player)
                val = world.pop_cell(pos)

                world.push_cell(next_loc, val)
                cell.on_entry(player, world)


