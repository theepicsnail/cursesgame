# -*- coding: utf-8 -*-
import curses
from menu import Menu
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
        pubsub.sub("engine:updateStatus", self.updateStatus)
        pubsub.sub("engine:updateSide", self.updateSide)
        pubsub.sub("engine:updateWindow", self.updateWindow)


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
        pubsub.pub("engine:updateSide")

    def updateStatus(self):
        # draw status bar
        self.status.erase()
        for idx, (item, count) in enumerate(self.world.player.list_items()):
            self.status.addstr(1, 4*idx, item.character.encode('utf-8'),
                    item.color)
            self.status.addstr("{:<3}".format(count))
        self.status.addstr(0, 0, \
            u"❤".encode('utf-8'), color(curses.COLOR_RED))
        #str(self.world.at(self.world.get_player())) + "  ")
#        self.status.addstr(
        self.status.addstr(": "+ str(self.world.get_player().get_hp()))
        self.status.refresh()

    def updateSide(self):
        # draw side bar
        self.side.erase()
        side_row = 0
        log_rows = self.side.getmaxyx()[0]
        for line in self.side_buffer[::-1]:
            if side_row >= log_rows:
                break
            self.side.addstr(side_row, 0, line[:37], 0)
            side_row += 1
        self.side.refresh()

    def updateWindow(self):
        self.window.erase()
        height, width = self.window.getmaxyx()
        world = self.world
        player = world.get_player()
        for row in xrange(-height/2, height/2):
            for col in xrange(-width/2, width/2):
                try:
                    cell = world.peek_cell(
                        world.relative_to(player, (row, col)))
                    self.window.addstr(row - - height/2, col - - width/2,
                        #row - -height/2, col - -width/2,
                        cell.character.encode('utf-8'), cell.color)
                except Exception:pass

        self.window.refresh()


    def mainloop(self):
        char = 0
        import levels.level1
        world = levels.level1.Level1()
        self.world = world
        player = world.get_player()
        player.set_hp(100)

        pubsub.pub("engine:updateWindow")

        self.playing = True
        def quit():
            self.playing = False
        menu = Menu([("Continue", lambda:0), ("Quit game", quit)], self.side)
        while self.playing:
            #handle input
            char = self.window.getch()
            update = False
            if char == 258: # Down
                update = world.move_south(player)
            elif char == 259: # Up
                update = world.move_north(player)
            elif char == 260: # left
                update = world.move_west(player)
            elif char == 261: # right
                update = world.move_east(player)
            elif char == 27: # escape
                menu.display()

            if update:
                pubsub.pub("engine:updateWindow")
