import curses, curses.wrapper
import locale

locale.setlocale(locale.LC_ALL,"")
curses.initscr()
curses.start_color()
curses.curs_set(0)

from util import color
import engine

def main(screen):
    try:
        engine.run()
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()


curses.wrapper(main)
