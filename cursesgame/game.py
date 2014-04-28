import curses, curses.wrapper
import locale

locale.setlocale(locale.LC_ALL, "")
curses.initscr()
curses.start_color()
curses.curs_set(0)


def main(screen):
    engine = None
    try:
        from engine import Engine
        engine = Engine()
        engine.mainloop()
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        if engine is not None:
            for line in engine.side_buffer:
                print line

curses.wrapper(main)
