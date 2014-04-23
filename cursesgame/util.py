import curses

pairs = []
def color(fg=curses.COLOR_WHITE, bg=curses.COLOR_BLACK):
    key = (fg, bg)
    pid = len(pairs)+1

    if key in pairs:
        return curses.color_pair(pairs.index(key)+1)

    curses.init_pair(pid, fg, bg)
    pairs.append(key)
    return curses.color_pair(pid)

