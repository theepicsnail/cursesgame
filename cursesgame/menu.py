"""
Modified from:
http://stackoverflow.com/questions/14200721/how-to-create-a-menu-and-submenus-in-python-curses
"""

import curses
from curses import panel

class Menu(object):

    def __init__(self, items, stdscreen):
        self.window = stdscreen.derwin(0,0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items
        self.items.append(('exit menu','exit'))

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items)-1

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()
        while True:
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = '%d. %s' % (index, item[0])
                self.window.addstr(1+index, 1, msg, mode)

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                self.items[self.position][1]()
                break
                #if self.position == len(self.items)-1:
                #else:
            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

            elif key == 27: # Escape
                break

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

