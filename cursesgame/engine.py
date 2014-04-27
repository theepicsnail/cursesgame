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
        player = Player(15, 15)
        import levels.level1
        world = levels.level1.Level1()
        while char != 27:
            self.window.erase()
            player_loc = player.get_pos()
            top = max(0, player_loc[0] - height/2)#min(world.height, height)/2)
            left = max(0, player_loc[1] - width/2)# min(world.width, width)/2)
            #draw the screen
            for row in xrange(top, top+height):
                if row >= world.height:
                    break
                for col in xrange(left, left+width):
                    if col >= world.width:
                        break
                    try:
                        cell = world.peek_cell(row, col)
                        self.window.addstr(row-top, col-left,
                            cell.character.encode('utf-8'), cell.color)
                    except Exception:pass
            self.window.addch(player_loc[0]-top, player_loc[1]-left, '@',
                    color(curses.COLOR_YELLOW) | curses.A_BOLD)
            # draw status bar
            self.status.erase()
            self.status.border(0, 0, 0, 0, 0, 0, 0, 0)
            self.status.addstr(1, 1, "Pos: {}".format(player_loc))
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
            next_loc = map(sum,zip(player_loc, direction))

            # collision detection
            # out of bounds
            if next_loc[0] < 0 or\
                next_loc[1] < 0 or\
                next_loc[0] >= world.height or\
                next_loc[1] >= world.width:
                continue

            cell = world.peek_cell(next_loc[0], next_loc[1])
            if cell.enterable_by(player, world, direction):
                player.set_pos(*next_loc)
                cell.on_entry(player, world)


