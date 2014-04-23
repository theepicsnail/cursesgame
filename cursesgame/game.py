import curses, curses.wrapper
import locale

locale.setlocale(locale.LC_ALL, "")
curses.initscr()
curses.start_color()
curses.curs_set(0)

from engine import Engine

def main(screen):
    engine = Engine()
    try:
        engine.mainloop()
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()


curses.wrapper(main)
